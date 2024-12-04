
mkdir -p bin
go build -o bin/heartbeat cmd/heartbeat/main.go
go build -o bin/test cmd/test/main.go
go build -o bin/check-heartbeat cmd/check-heartbeat/main.go