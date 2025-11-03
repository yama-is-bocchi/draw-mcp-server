# draw-mcp-server

A simple MCP (Model Context Protocol) server that can be easily run using Docker.

## Usage

Follow the steps below to set up and run the server.

```bash
# 1. Clone the repository
git clone https://github.com/yama-is-bocchi/draw-mcp-server.git
cd draw-mcp-server

# 2. Create a .env file
# Required environment variable:
TRANSPORT=sse

# Optional environment variables for Basic Authentication:
USERNAME=your_username
PASSWORD=your_password
# If USERNAME and PASSWORD are set, Basic Authentication will be applied to image access.

# 3. Start the server using Docker
docker compose up -d
```

The server will start and be ready to handle MCP requests.

## Configuration

After starting the server, configure your MCP client as follows:

```json
{
  "mcpServers": {
    "draw-mcp": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## License

This project is licensed under the MIT License.
