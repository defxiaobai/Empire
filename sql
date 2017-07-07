CREATE DATABASE taiyang DEFAULT CHARACTER set utf8 COLLATE utf8_general_ci

CREATE table zhidao(
	id int(11) unsigned not null AUTO_INCREMENT,
    title varchar(200) not null,
    content text not null,
    url varchar(120) not null,
    PRIMARY KEY(id)
)ENGINE=INNODB DEFAULT charset = UTF8;


CREATE table toutiao(
	id int(11) unsigned not null AUTO_INCREMENT,
    title varchar(200) not null,
    content text not null,
    url varchar(120) not null,
    PRIMARY KEY(id)
)ENGINE=INNODB DEFAULT charset = UTF8;


