FROM golang:1.26-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o main ./cmd/server

FROM alpine:3.21

WORKDIR /app

COPY --from=builder /app/main ./main
COPY --from=builder /app/migrations ./migrations
COPY --from=builder /app/docs ./docs

RUN adduser -D -H -u 10001 appuser \
	&& chown -R appuser:appuser /app

USER appuser

EXPOSE 8004

CMD ["./main"]