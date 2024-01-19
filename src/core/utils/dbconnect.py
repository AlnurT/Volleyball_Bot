import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name, game, extra_players):
        query = f"""
                DO
                $do$
                    BEGIN
                       IF EXISTS(SELECT user_id FROM players WHERE user_id = {user_id}) THEN
                          UPDATE players SET game={game} WHERE user_id = {user_id};
                       ELSE
                          INSERT INTO players (user_id, user_name, game, extra_players)
                          VALUES ({user_id}, '{user_name}', {game}, {extra_players});
                       END IF;
                    END
                $do$
        """
        await self.connector.execute(query)
