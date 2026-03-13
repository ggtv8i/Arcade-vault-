#!/bin/bash
echo "=========================================="
echo "  Arcade Vault — Simple HTTP Server"
echo "=========================================="
echo "  http://localhost:8080/index.html"
echo "  Ctrl+C للإيقاف"
echo "=========================================="
python3 -m http.server 8080 || python -m http.server 8080
