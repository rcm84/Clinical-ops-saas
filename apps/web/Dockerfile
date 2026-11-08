# Web (Next.js 14) — PR 1: multi-stage build with standalone output.
# Requires `output: 'standalone'` in next.config.mjs (set in PR 1).
# PR 2: NEXT_PUBLIC_CLINICAL_CORE_URL se hornea en el build (variable
# NEXT_PUBLIC_*); por defecto apunta a localhost:4000 para compose local.
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

FROM node:20-alpine AS builder
WORKDIR /app
ARG NEXT_PUBLIC_CLINICAL_CORE_URL=http://localhost:4000
ENV NEXT_PUBLIC_CLINICAL_CORE_URL=$NEXT_PUBLIC_CLINICAL_CORE_URL
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
