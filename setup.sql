/*
 * create_table.sql
 * Copyright (C) 2018 weihao <blackhatdwh@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */
DROP DATABASE Patent;
CREATE DATABASE Patent;
USE Patent
CREATE TABLE Patent (
    title VARCHAR(100),
    app_num VARCHAR(20),
    app_date DATE,
    pub_num VARCHAR(20),
    pub_date DATE,
    IPC VARCHAR(10),
    app_person VARCHAR(20),
    invent_person VARCHAR(20),
    agent_person VARCHAR(20),
    agent_inst VARCHAR(20),
    priority_num VARCHAR(20),
    priority_date DATE,
    app_addr VARCHAR(50),
    abstract VARCHAR(500),
    content TEXT,
    pub_state VARCHAR(10),
    similar INTEGER,
    reference INTEGER,
    cited INTEGER
);

-- vim:et
