FROM golang:1.26-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o main ./cmd/server

FROM alpine:3.21

WORKDIR /root/

COPY --from=builder /app/main .

RUN adduser -D -H -u 10001 appuser
USER appuser

EXPOSE 8003

CMD ["./main"]