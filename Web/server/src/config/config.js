module.exports = {
    port: process.env.PORT || 8081,
    db: {
        datanbase: process.env.DB_NAME || 'BingoBot',
        user: process.env.DB_USER || 'BingoBot',
        password: process.env.DB_PASS || 'BingoBot',
        options: {
            dialect: process.env.DIALECT || 'sqlite',
            host: process.env.HOST || 'localhost',
            storage: './BingoBot.sqlite'
        }
    }
}
