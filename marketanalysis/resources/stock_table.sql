CREATE TABLE {{ table_name }}(
    yyyymmdd int primary key,
    date date,
    open float,
    high float,
    low float,
    close float,
    adj_close float,
    volume float
)