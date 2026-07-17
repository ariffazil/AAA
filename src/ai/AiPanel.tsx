import { useEffect, useMemo, useState } from 'react';
import {
  Bot,
  BrainCircuit,
  DatabaseZap,
  FileUp,
  LoaderCircle,
  ScanSearch,
  ScrollText,
  Send,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import {
  getAiHealth,
  getAiModels,
  queryAiDocuments,
  streamAiChat,
  uploadAiDocument,
  type AiCitation,
  type AiHealth,
  type AiMessage,
  type AiModel,
  type AiProvider,
} from './client';

interface ChatTurn extends AiMessage {
  id: string;
  citations?: AiCitation[];
}

const PROVIDER_LABELS: Record<AiProvider, { title: string; eyebrow: string }> = {
  ollama: {
    title: 'Local Ollama',
    eyebrow: 'Direct model runtime',
  },
  arifos: {
    title: 'arifOS governed',
    eyebrow: 'Constitutional response path',
  },
  openrouter: {
    title: 'OpenRouter',
    eyebrow: '365 models via API',
  },
};

function formatBytes(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes <= 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  const exponent = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const value = bytes / 1024 ** exponent;
  return `${value.toFixed(value >= 10 || exponent === 0 ? 0 : 1)} ${units[exponent]}`;
}

function relativeTimestamp(input: string | null): string {
  if (!input) return 'unknown';
  const timestamp = new Date(input).getTime();
  if (Number.isNaN(timestamp)) return 'unknown';
  const minutes = Math.round((Date.now() - timestamp) / 60000);
  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.round(hours / 24)}d ago`;
}

export default function AiPanel() {
  const [health, setHealth] = useState<AiHealth | null>(null);
  const [models, setModels] = useState<AiModel[]>([]);
  const [selectedModel, setSelectedModel] = useState('qwen2.5:7b');
  const [provider, setProvider] = useState<AiProvider>('ollama');
  const [messages, setMessages] = useState<ChatTurn[]>([
    {
      id: crypto.randomUUID(),
      role: 'assistant',
      content:
        'AAA AI workspace is live. Use Local Ollama for direct inference, or arifOS governed mode for constitutional composition. Upload docs to ground replies in your own corpus.',
    },
  ]);
  const [draft, setDraft] = useState('');
  const [ragQuery, setRagQuery] = useState('');
  const [citations, setCitations] = useState<AiCitation[]>([]);
  const [groundWithLatestRetrieval, setGroundWithLatestRetrieval] = useState(true);
  const [isBooting, setIsBooting] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadNote, setUploadNote] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function boot() {
      try {
        const [healthPayload, modelsPayload] = await Promise.all([getAiHealth(), getAiModels()]);
        if (cancelled) return;
        setHealth(healthPayload);
        setModels(modelsPayload.models);
        setSelectedModel((current) => current || modelsPayload.defaults.model);
      } catch (bootError) {
        if (cancelled) return;
        setError(bootError instanceof Error ? bootError.message : 'Failed to initialize AI workspace');
      } finally {
        if (!cancelled) setIsBooting(false);
      }
    }

    void boot();
    return () => {
      cancelled = true;
    };
  }, []);

  const currentProvider = useMemo(() => PROVIDER_LABELS[provider], [provider]);

  async function handleRetrievalSearch(queryOverride?: string): Promise<AiCitation[]> {
    const query = (queryOverride ?? ragQuery).trim();
    if (!query) {
      setCitations([]);
      return [];
    }

    setIsSearching(true);
    setError(null);
    try {
      const response = await queryAiDocuments(query, 5);
      setCitations(response.citations);
      setRagQuery(query);
      return response.citations;
    } catch (searchError) {
      setError(searchError instanceof Error ? searchError.message : 'Document search failed');
      return [];
    } finally {
      setIsSearching(false);
    }
  }

  async function handleUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadNote(null);
    setError(null);

    try {
      const content = await file.text();
      const response = await uploadAiDocument({
        filename: file.name,
        content,
        mimeType: file.type || 'text/plain',
      });

      setUploadNote(`${response.document.filename} indexed into ${response.document.chunks} chunks.`);
      setRagQuery(file.name);
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : 'Document upload failed');
    } finally {
      setIsUploading(false);
      event.target.value = '';
    }
  }

  async function handleSend() {
    const prompt = draft.trim();
    if (!prompt || isSending) return;

    const userTurn: ChatTurn = {
      id: crypto.randomUUID(),
      role: 'user',
      content: prompt,
    };
    const assistantId = crypto.randomUUID();

    setDraft('');
    setError(null);
    setIsSending(true);
    setMessages((current) => [
      ...current,
      userTurn,
      {
        id: assistantId,
        role: 'assistant',
        content: '',
      },
    ]);

    try {
      const liveCitations = groundWithLatestRetrieval ? await handleRetrievalSearch(prompt) : citations;

      await streamAiChat({
        provider,
        model: selectedModel,
        citations: liveCitations,
        messages: [...messages, userTurn].map((message) => ({
          role: message.role,
          content: message.content,
        })),
        onChunk: (chunk) => {
          setMessages((current) =>
            current.map((message) =>
              message.id === assistantId
                ? {
                    ...message,
                    content: message.content + chunk,
                  }
                : message
            )
          );
        },
        onDone: ({ citations: doneCitations }) => {
          setMessages((current) =>
            current.map((message) =>
              message.id === assistantId
                ? {
                    ...message,
                    citations: doneCitations,
                  }
                : message
            )
          );
        },
      });
    } catch (chatError) {
      setMessages((current) =>
        current.map((message) =>
          message.id === assistantId
            ? {
                ...message,
                content: 'Response failed before completion.',
              }
            : message
        )
      );
      setError(chatError instanceof Error ? chatError.message : 'Chat failed');
    } finally {
      setIsSending(false);
    }
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#090806] text-white">
      <div className="pointer-events-none absolute inset-0 toroid-bg rings-bg opacity-80" />
      <div className="pointer-events-none absolute inset-0 spiral-grid opacity-30" />

      <section className="relative mx-auto flex w-full max-w-[1440px] flex-col gap-6 px-4 pb-10 pt-28 md:px-6 xl:px-8">
        <header className="glass-gold relative overflow-hidden rounded-[28px] border border-[rgba(212,168,83,0.18)] px-6 py-6 shadow-[0_30px_120px_rgba(0,0,0,0.35)] md:px-8">
          <div className="absolute inset-y-0 right-0 w-[36%] bg-[radial-gradient(circle_at_top_right,rgba(58,158,168,0.25),transparent_58%)]" />
          <div className="relative flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl space-y-4">
              <div className="inline-flex items-center gap-2 rounded-full border border-[rgba(212,168,83,0.18)] bg-black/30 px-3 py-1 text-[11px] uppercase tracking-[0.28em] text-gold-bright">
                <Sparkles className="h-3.5 w-3.5" />
                AAA native AI workspace
              </div>
              <div>
                <h1 className="gradient-text-gold text-4xl font-black tracking-[-0.04em] md:text-6xl">
                  #ai cockpit
                </h1>
                <p className="mt-3 max-w-2xl text-sm text-[rgba(255,255,255,0.62)] md:text-base">
                  One surface for local inference, governed composition, document grounding, and
                  live model control. No iframe. No sidecar UI. Native AAA steel.
                </p>
              </div>
            </div>

            <div className="grid gap-3 md:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-black/30 px-4 py-3">
                <div className="text-[10px] uppercase tracking-[0.24em] text-white/40">Provider</div>
                <div className="mt-2 flex items-center gap-2 text-sm font-semibold text-white">
                  <ShieldCheck className="h-4 w-4 text-gold-bright" />
                  {currentProvider.title}
                </div>
                <div className="mt-1 text-xs text-white/45">{currentProvider.eyebrow}</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-black/30 px-4 py-3">
                <div className="text-[10px] uppercase tracking-[0.24em] text-white/40">Models online</div>
                <div className="mt-2 flex items-center gap-2 text-sm font-semibold text-white">
                  <Bot className="h-4 w-4 text-[#63d3dc]" />
                  {models.length || 0} live tags
                </div>
                <div className="mt-1 text-xs text-white/45">
                  default {selectedModel || health?.defaults.chat_model || 'qwen2.5:7b'}
                </div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-black/30 px-4 py-3">
                <div className="text-[10px] uppercase tracking-[0.24em] text-white/40">Retrieval</div>
                <div className="mt-2 flex items-center gap-2 text-sm font-semibold text-white">
                  <DatabaseZap className="h-4 w-4 text-[#63d3dc]" />
                  {health?.defaults.rag_collection ?? 'aaa_ai_docs'}
                </div>
                <div className="mt-1 text-xs text-white/45">
                  {citations.length} citations in current working set
                </div>
              </div>
            </div>
          </div>
        </header>

        <div className="grid gap-6 xl:grid-cols-[minmax(0,1.7fr)_420px]">
          <section className="glass-gold rounded-[28px] border border-[rgba(212,168,83,0.14)] p-4 md:p-5">
            <div className="flex flex-col gap-4 border-b border-white/10 pb-4 md:flex-row md:items-end md:justify-between">
              <div>
                <div className="text-[11px] uppercase tracking-[0.24em] text-white/40">Live chat lane</div>
                <h2 className="mt-1 text-2xl font-black tracking-[-0.03em] text-white">
                  Direct inference or governed response
                </h2>
              </div>

              <div className="flex flex-wrap gap-2">
                {(['ollama', 'arifos'] as AiProvider[]).map((option) => (
                  <button
                    key={option}
                    type="button"
                    onClick={() => setProvider(option)}
                    className={`rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] transition ${
                      provider === option
                        ? 'bg-[#d4a853] text-black shadow-[0_0_20px_rgba(212,168,83,0.25)]'
                        : 'border border-white/10 bg-black/30 text-white/60 hover:border-[rgba(212,168,83,0.24)] hover:text-white'
                    }`}
                  >
                    {PROVIDER_LABELS[option].title}
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <label className="flex min-w-0 flex-1 flex-col gap-2">
                <span className="text-[11px] uppercase tracking-[0.24em] text-white/40">Model selector</span>
                <select
                  value={selectedModel}
                  onChange={(event) => setSelectedModel(event.target.value)}
                  disabled={provider === 'arifos'}
                  className="rounded-2xl border border-white/10 bg-black/50 px-4 py-3 text-sm text-white outline-none transition focus:border-[rgba(212,168,83,0.38)] disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {models.length === 0 ? (
                    <option value={health?.defaults.chat_model ?? 'qwen2.5:7b'}>
                      {health?.defaults.chat_model ?? 'qwen2.5:7b'}
                    </option>
                  ) : (
                    models.map((model) => (
                      <option key={model.name} value={model.name}>
                        {model.name}
                      </option>
                    ))
                  )}
                </select>
              </label>

              <div className="grid gap-2 md:min-w-[280px]">
                <div className="flex items-center justify-between rounded-2xl border border-white/10 bg-black/30 px-4 py-3">
                  <div>
                    <div className="text-[11px] uppercase tracking-[0.24em] text-white/40">Ground with retrieval</div>
                    <div className="mt-1 text-xs text-white/50">
                      Attach latest semantic hits before answering
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setGroundWithLatestRetrieval((current) => !current)}
                    className={`h-8 w-14 rounded-full border transition ${
                      groundWithLatestRetrieval
                        ? 'border-[rgba(212,168,83,0.36)] bg-[rgba(212,168,83,0.18)]'
                        : 'border-white/10 bg-black/50'
                    }`}
                  >
                    <span
                      className={`block h-6 w-6 rounded-full bg-white shadow transition ${
                        groundWithLatestRetrieval ? 'translate-x-6 bg-[#d4a853]' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              </div>
            </div>

            <div className="mt-5 space-y-3 rounded-[24px] border border-white/10 bg-[rgba(6,6,5,0.8)] p-3 md:p-4">
              <div className="max-h-[560px] space-y-3 overflow-y-auto pr-1">
                {messages.map((message) => (
                  <article
                    key={message.id}
                    className={`rounded-[22px] border px-4 py-4 ${
                      message.role === 'assistant'
                        ? 'border-[rgba(212,168,83,0.16)] bg-[linear-gradient(180deg,rgba(19,18,15,0.92),rgba(11,10,8,0.92))]'
                        : 'border-[rgba(58,158,168,0.2)] bg-[linear-gradient(180deg,rgba(9,22,24,0.55),rgba(7,13,15,0.55))]'
                    }`}
                  >
                    <div className="mb-2 flex items-center gap-2 text-[10px] uppercase tracking-[0.28em] text-white/40">
                      {message.role === 'assistant' ? (
                        <>
                          <BrainCircuit className="h-3.5 w-3.5 text-gold-bright" />
                          Assistant
                        </>
                      ) : (
                        <>
                          <ScrollText className="h-3.5 w-3.5 text-[#63d3dc]" />
                          Operator
                        </>
                      )}
                    </div>
                    <p className="mb-0 whitespace-pre-wrap text-sm leading-7 text-white/88">
                      {message.content || (message.role === 'assistant' && isSending ? 'Thinking…' : '')}
                    </p>

                    {message.citations && message.citations.length > 0 ? (
                      <div className="mt-4 grid gap-2 md:grid-cols-2">
                        {message.citations.map((citation) => (
                          <div
                            key={`${message.id}-${citation.id}`}
                            className="rounded-2xl border border-white/8 bg-black/30 px-3 py-3 text-xs text-white/60"
                          >
                            <div className="flex items-center justify-between gap-2">
                              <span className="font-semibold text-white/80">{citation.filename}</span>
                              <span className="text-[10px] uppercase tracking-[0.2em] text-gold-bright">
                                {citation.score.toFixed(2)}
                              </span>
                            </div>
                            <p className="mt-2 mb-0 line-clamp-4 whitespace-pre-wrap text-white/52">
                              {citation.snippet}
                            </p>
                          </div>
                        ))}
                      </div>
                    ) : null}
                  </article>
                ))}
              </div>

              <div className="rounded-[24px] border border-white/10 bg-black/40 p-3">
                <textarea
                  value={draft}
                  onChange={(event) => setDraft(event.target.value)}
                  placeholder="Ask AAA anything — runtime, documents, or direct model inference."
                  className="min-h-[132px] w-full resize-none bg-transparent text-sm leading-7 text-white outline-none placeholder:text-white/28"
                />
                <div className="mt-3 flex flex-col gap-3 border-t border-white/10 pt-3 md:flex-row md:items-center md:justify-between">
                  <div className="text-xs text-white/45">
                    {provider === 'arifos'
                      ? 'Governed mode resolves through the arifOS federation gateway.'
                      : 'Local mode streams tokens straight from Ollama through the AAA backend.'}
                  </div>
                  <button
                    type="button"
                    onClick={() => void handleSend()}
                    disabled={!draft.trim() || isSending || isBooting}
                    className="inline-flex items-center justify-center gap-2 rounded-full bg-[#d4a853] px-5 py-3 text-xs font-black uppercase tracking-[0.24em] text-black transition hover:brightness-105 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {isSending ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                    transmit
                  </button>
                </div>
              </div>
            </div>
          </section>

          <aside className="space-y-6">
            <section className="glass-gold rounded-[28px] border border-[rgba(212,168,83,0.14)] p-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="text-[11px] uppercase tracking-[0.24em] text-white/40">Semantic grounding</div>
                  <h3 className="mt-1 text-xl font-black tracking-[-0.03em] text-white">RAG dock</h3>
                </div>
                <DatabaseZap className="h-5 w-5 text-gold-bright" />
              </div>

              <div className="mt-4 space-y-4">
                <label className="flex cursor-pointer items-center justify-center gap-3 rounded-[22px] border border-dashed border-[rgba(212,168,83,0.28)] bg-black/30 px-4 py-4 text-sm text-white/70 transition hover:border-[rgba(212,168,83,0.5)] hover:text-white">
                  <FileUp className="h-4 w-4 text-gold-bright" />
                  {isUploading ? 'Indexing document…' : 'Upload text, markdown, JSON, CSV, or notes'}
                  <input type="file" className="hidden" onChange={(event) => void handleUpload(event)} />
                </label>

                {uploadNote ? (
                  <div className="rounded-2xl border border-[rgba(58,158,168,0.2)] bg-[rgba(12,30,32,0.42)] px-4 py-3 text-sm text-[#b8f1f5]">
                    {uploadNote}
                  </div>
                ) : null}

                <label className="block">
                  <span className="text-[11px] uppercase tracking-[0.24em] text-white/40">Ask your corpus</span>
                  <textarea
                    value={ragQuery}
                    onChange={(event) => setRagQuery(event.target.value)}
                    placeholder="Search across uploaded documents"
                    className="mt-2 min-h-[96px] w-full resize-none rounded-[22px] border border-white/10 bg-black/40 px-4 py-3 text-sm text-white outline-none placeholder:text-white/28 focus:border-[rgba(212,168,83,0.35)]"
                  />
                </label>

                <button
                  type="button"
                  onClick={() => void handleRetrievalSearch()}
                  disabled={!ragQuery.trim() || isSearching}
                  className="inline-flex w-full items-center justify-center gap-2 rounded-full border border-[rgba(212,168,83,0.24)] bg-[rgba(212,168,83,0.08)] px-4 py-3 text-xs font-black uppercase tracking-[0.22em] text-gold-bright transition hover:bg-[rgba(212,168,83,0.12)] disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isSearching ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <ScanSearch className="h-4 w-4" />}
                  retrieve
                </button>

                <div className="space-y-3">
                  {citations.length === 0 ? (
                    <div className="rounded-[22px] border border-white/10 bg-black/20 px-4 py-5 text-sm text-white/45">
                      No retrieval hits yet. Upload a document, then query it here or let the chat
                      auto-ground responses.
                    </div>
                  ) : (
                    citations.map((citation) => (
                      <article
                        key={citation.id}
                        className="rounded-[22px] border border-white/10 bg-black/30 px-4 py-4"
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <div className="text-sm font-semibold text-white">{citation.filename}</div>
                            <div className="mt-1 text-[10px] uppercase tracking-[0.22em] text-white/35">
                              chunk {citation.chunk_index + 1}
                            </div>
                          </div>
                          <div className="rounded-full border border-[rgba(212,168,83,0.18)] px-2 py-1 text-[10px] font-semibold tracking-[0.2em] text-gold-bright">
                            {citation.score.toFixed(2)}
                          </div>
                        </div>
                        <p className="mt-3 mb-0 whitespace-pre-wrap text-xs leading-6 text-white/58">
                          {citation.snippet}
                        </p>
                      </article>
                    ))
                  )}
                </div>
              </div>
            </section>

            <section className="glass-gold rounded-[28px] border border-[rgba(212,168,83,0.14)] p-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="text-[11px] uppercase tracking-[0.24em] text-white/40">Surface status</div>
                  <h3 className="mt-1 text-xl font-black tracking-[-0.03em] text-white">Runtime edges</h3>
                </div>
                <Sparkles className="h-5 w-5 text-gold-bright" />
              </div>

              <div className="mt-4 grid gap-3">
                {[
                  ['ollama', health?.upstreams.ollama ?? (isBooting ? 'probing' : 'unknown')],
                  ['arifOS', health?.upstreams.arifos ?? (isBooting ? 'probing' : 'unknown')],
                  ['qdrant', health?.upstreams.qdrant ?? (isBooting ? 'probing' : 'unknown')],
                ].map(([label, status]) => (
                  <div
                    key={label}
                    className="flex items-center justify-between rounded-2xl border border-white/10 bg-black/30 px-4 py-3"
                  >
                    <span className="text-sm text-white/70">{label}</span>
                    <span
                      className={`rounded-full px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] ${
                        status === 'healthy'
                          ? 'bg-[rgba(75,138,63,0.22)] text-[#baf29f]'
                          : status === 'configured'
                            ? 'bg-[rgba(58,158,168,0.18)] text-[#98ebf1]'
                            : 'bg-[rgba(212,168,83,0.16)] text-gold-bright'
                      }`}
                    >
                      {status}
                    </span>
                  </div>
                ))}
              </div>

              <div className="mt-4 rounded-[22px] border border-white/10 bg-black/20 px-4 py-4 text-xs leading-6 text-white/52">
                <p className="mb-2">
                  <strong className="text-white/78">Vision lane:</strong> upload UI is intentionally
                  deferred until a multimodal model exists in Ollama.
                </p>
                <p className="mb-0">
                  Current default model snapshot was last updated{' '}
                  {relativeTimestamp(models.find((model) => model.name === selectedModel)?.modified_at ?? null)}.
                </p>
              </div>

              {error ? (
                <div className="mt-4 rounded-[22px] border border-[rgba(255,98,98,0.22)] bg-[rgba(60,12,12,0.45)] px-4 py-3 text-sm text-[#ffb7b7]">
                  {error}
                </div>
              ) : null}
            </section>

            <section className="glass-gold rounded-[28px] border border-[rgba(212,168,83,0.14)] p-5">
              <div className="text-[11px] uppercase tracking-[0.24em] text-white/40">Live model inventory</div>
              <div className="mt-4 space-y-3">
                {models.length === 0 ? (
                  <div className="rounded-[22px] border border-white/10 bg-black/20 px-4 py-5 text-sm text-white/45">
                    {isBooting ? 'Loading models…' : 'No models reported by Ollama.'}
                  </div>
                ) : (
                  models.map((model) => (
                    <div
                      key={model.name}
                      className={`rounded-[22px] border px-4 py-4 ${
                        selectedModel === model.name
                          ? 'border-[rgba(212,168,83,0.3)] bg-[rgba(212,168,83,0.08)]'
                          : 'border-white/10 bg-black/20'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <div className="text-sm font-semibold text-white">{model.name}</div>
                          <div className="mt-1 text-[10px] uppercase tracking-[0.22em] text-white/35">
                            {relativeTimestamp(model.modified_at)}
                          </div>
                        </div>
                        <div className="text-xs text-gold-bright">{formatBytes(model.size)}</div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </section>
          </aside>
        </div>
      </section>
    </main>
  );
}
