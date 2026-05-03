FROM node:22-alpine
WORKDIR /app
COPY package.json .
RUN npm install --omit=dev
COPY server.js .
COPY vault.js .
COPY agent-cards/ ./agent-cards/
EXPOSE 3001
ENV PORT=3001
CMD ["node", "server.js"]