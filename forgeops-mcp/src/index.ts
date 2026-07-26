/**
 * ForgeOps MCP Server
 *
 * AI Decision Workbench backend for Smart Manufacturing.
 * Built with NitroStack TypeScript SDK.
 *
 * Transport:
 * - Development: STDIO (for MCP clients like Claude Desktop)
 * - Production: Dual transport (STDIO + HTTP SSE)
 */

import 'dotenv/config';
import { McpApplicationFactory } from './nitrostack.js';
import { AppModule } from './app.module.js';

// Catch unhandled exceptions to ensure they are logged for NitroStack
process.on('uncaughtException', (err) => {
  console.error('❌ Uncaught Exception:', err);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Rejection at:', promise, 'reason:', reason);
});

async function bootstrap() {
  const server = await McpApplicationFactory.create(AppModule);
  await server.start();

  // Attach /health endpoint for NitroStack monitoring
  const httpTransport = server.getHttpTransport();
  if (httpTransport && httpTransport.getApp) {
    const app = httpTransport.getApp();
    app.get('/health', (req, res) => {
      res.status(200).json({ status: 'healthy', service: 'forgeops-mcp' });
    });
    console.log('✅ HTTP /health endpoint registered for NitroStack monitoring');
  }
}

bootstrap().catch((error) => {
  console.error('❌ ForgeOps MCP Server failed to start:', error);
  process.exit(1);
});
