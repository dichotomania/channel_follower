import psycopg2

#資料庫連線測試
conn = psycopg2.connect(database = "dfk7f1v6svu5vl",
                        user = "cdunivoierylhd",
                        password = "b650b5644d343c775f2ba9e24358f246dfb9052d5b1f90e5e0ad9c2dd3c6766a",
                        host = "ec2-44-194-113-156.compute-1.amazonaws.com",
                        port = "5432")
cur = conn.cursor()

cur.execute("SELECT VERSION()")
results = cur.fetchall()
print("Database version:%s" % results)

conn.commit()
cur.close()

#PostgreSQL建表
def create_tables():
    commands = (
        '''CREATE TABLE userinfo(
            UserId VARCHAR(255) PRIMARY KEY,
            UserName VARCHAR(255) NOT NULL,
            Channel1 VARCHAR(255) ,
            Channel2 VARCHAR(255) ,
            Channel3 VARCHAR(255) ,
            Videos VARCHAR(50) )''',
    
        '''CREATE TABLE yotuber(
            ChannelName VARCHAR(255) PRIMARY KEY,
            Channel_id VARCHAR(255) NOT NULL,
            Type VARCHAR(20) NOT NULL,
            Videos_id VARCHAR(255) NOT NULL)''',
    
        '''CREATE TABLE video_info(
            Id VARCHAR(255) PRIMARY KEY,
            VideoName VARCHAR(255) NOT NULL,
            PublishedTime VARCHAR(255) NOT NULL,
            Picture VARCHAR(255) NOT NULL)
            '''
        )
    
    try:
        conn = psycopg2.connect(database = "dfk7f1v6svu5vl",
                        user = "cdunivoierylhd",
                        password = "b650b5644d343c775f2ba9e24358f246dfb9052d5b1f90e5e0ad9c2dd3c6766a",
                        host = "ec2-44-194-113-156.compute-1.amazonaws.com",
                        port = "5432")
        cur = conn.cursor()
        
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()
            
if __name__ == ("__main__"):
    create_tables()