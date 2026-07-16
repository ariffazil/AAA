/**
 * MCP Apps Sandbox Proxy — G3 double-iframe (SEP-1865)
 * =====================================================
 * Outer iframe (proxy): allow-scripts + allow-same-origin, unique srcdoc doc
 *   → receives host messages, loads guest, filters sandbox-* traffic
 * Inner iframe (guest): allow-scripts ONLY (no same-origin)
 *   → cannot escape sandbox by removing attributes on itself
 *
 * Host never talks to guest directly. Guest never holds secrets.
 *
 * PLAN: DIRECTIVE-GEOX-MCP-WELL-DESK-P0-PLUS · G3
 * DITEMPA BUKAN DIBERI
 */

/** Restrictive default when resource does not declare CSP */
export const DEFAULT_GUEST_CSP = [
  "default-src 'none'",
  "script-src 'unsafe-inline'",
  "style-src 'unsafe-inline'",
  "img-src data: blob:",
  "font-src data:",
  "connect-src 'none'",
  "frame-src 'none'",
  "base-uri 'none'",
  "form-action 'none'",
  "object-src 'none'",
].join("; ");

/**
 * Build srcdoc for the outer Sandbox Proxy page.
 * Must be self-contained (no external scripts).
 */
export function buildSandboxProxySrcdoc(): string {
  // Compact, no template injection of untrusted data — guest HTML arrives via postMessage.
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>MCP Sandbox Proxy</title>
<style>html,body{margin:0;height:100%;background:#0b0f14}#g{width:100%;height:100%;border:0;display:block}</style>
</head>
<body>
<script>
(function(){
  "use strict";
  var guest=null;
  var loaded=false;
  function isRpc(d){
    if(typeof d==="string"){try{d=JSON.parse(d)}catch(e){return null}}
    if(!d||d.jsonrpc!=="2.0")return null;
    return d;
  }
  // Uses "*" targetOrigin because this proxy iframe has sandbox="allow-scripts"
  // (no allow-same-origin), giving it a null/unique origin. A specific
  // targetOrigin would silent-drop. Safe because:
  //   1. parent is the AAA host that created this iframe — we trust it
  //   2. guest is our own inner iframe with connect-src 'none'
  //   3. Host validates event.source + event.origin on receiving end
  function toHost(msg){
    try{parent.postMessage(msg,"*")}catch(e){}
  }
  function toGuest(msg){
    if(guest&&guest.contentWindow){
      try{guest.contentWindow.postMessage(msg,"*")}catch(e){}
    }
  }
  function injectCsp(html,csp){
    if(!html)return html;
    if(/http-equiv\\s*=\\s*["']?Content-Security-Policy/i.test(html))return html;
    var meta='<meta http-equiv="Content-Security-Policy" content="'+String(csp||"").replace(/"/g,"&quot;")+'">';
    if(/<head[^>]*>/i.test(html))return html.replace(/<head[^>]*>/i,function(m){return m+meta});
    return meta+html;
  }
  function loadGuest(params){
    params=params||{};
    var html=injectCsp(params.html||"",params.csp||"");
    if(guest){try{guest.remove()}catch(e){}}
    guest=document.createElement("iframe");
    guest.id="g";
    guest.setAttribute("sandbox","allow-scripts");
    guest.setAttribute("allow","");
    guest.setAttribute("referrerpolicy","no-referrer");
    guest.srcdoc=html;
    document.body.appendChild(guest);
    loaded=true;
    toHost({jsonrpc:"2.0",method:"ui/notifications/sandbox-ready",params:{ok:true,g3:true}});
  }
  window.addEventListener("message",function(ev){
    var data=isRpc(ev.data);
    if(!data)return;
    var method=data.method||"";
    // From host (parent)
    if(ev.source===parent){
      if(method==="ui/notifications/sandbox-load"){
        loadGuest(data.params||{});
        return;
      }
      // Never inject sandbox-control into guest
      if(method.indexOf("ui/notifications/sandbox-")===0)return;
      toGuest(data);
      return;
    }
    // From guest
    if(guest&&ev.source===guest.contentWindow){
      // Drop internal sandbox traffic if guest spoofs it
      if(method.indexOf("ui/notifications/sandbox-")===0)return;
      toHost(data);
    }
  });
  toHost({jsonrpc:"2.0",method:"ui/notifications/sandbox-boot",params:{ok:true,g3:true}});
})();
</script>
</body>
</html>`;
}

/** Methods the host will accept from the proxy (origin: guest, via proxy). */
export const ALLOWED_VIEW_METHODS = new Set([
  "ui/initialize",
  "ui/notifications/initialized",
  "tools/call",
  "resources/read",
  "ui/update-model-context",
  "ui/open-link",
  "ui/message",
  "ui/resource-teardown",
]);

/** Internal sandbox methods (proxy ↔ host only). */
export const SANDBOX_METHODS = new Set([
  "ui/notifications/sandbox-boot",
  "ui/notifications/sandbox-ready",
  "ui/notifications/sandbox-load",
]);
