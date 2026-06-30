FROM node:22-alpine
WORKDIR /app
COPY package.json .
RUN npm install --omit=dev
COPY server.js .
COPY vault.js .
COPY agent-cards/ ./agent-cards/
EXPOSE 3001
ENV PORT=3001

LABEL org.opencontainers.image.source="https://github.com/ariffazil/AAA" \
      org.opencontainers.image.description="Control plane — A2A gateway, cockpit dashboard" \
      org.opencontainers.image.version="2026.06.30" \
      org.opencontainers.image.licenses="BSL-1.1" \
      arifos.organ="AAA" \
      arifos.authority="F13_SOVEREIGN"

CMD ["node", "server.js"]