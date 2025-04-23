from aiohttp import web

async def health(request):
    return web.Response(text="ok", content_type="text/plain")

async def demo(request):
    return web.Response(text="<h1>Mention Bot is running!</h1><p>This is a demo/health endpoint for Koyeb/Heroku deployment.</p>", content_type="text/html")

def setup_web_app():
    app = web.Application()
    app.router.add_get("/", demo)
    app.router.add_get("/health", health)
    return app

if __name__ == "__main__":
    import asyncio
    from aiogram import executor
    from bot.__main__ import dp, on_startup
    app = setup_web_app()
    web.run_app(app, port=8080)
    # The bot will be started by the main entrypoint as usual
