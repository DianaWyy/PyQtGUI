drop database if exists blsQcew;
create database blsQcew;
use blsQcew;

CREATE TABLE combined_quarters(
    id int PRIMARY KEY,
    own_code int REFERENCES own_titles(own_code),
    industry_code varchar(10) REFERENCES industry_titles(industry_code),
    agglvl_code int REFERENCES agglvl_titles(agglvl_code),
    year int,
    qtr int,
    disclosure_code varchar(5),
    qtrly_estabs int,
    month1_emplvl int,
    month2_emplvl int,
    month3_emplvl int,
    total_qtrly_wages bigint,
    avg_wkly_wage int
);

CREATE TABLE combined_annuals(
    id int,
    own_code int REFERENCES own_titles(own_code),
    industry_code varchar(10) REFERENCES industry_titles(industry_code),
    agglvl_code int REFERENCES agglvl_titles(agglvl_code),
    year int,
    disclosure_code varchar(5),
    annual_avg_estabs int,
    annual_avg_emplvl int,
    annual_avg_wkly_wage int,
    avg_annual_pay int,
    PRIMARY KEY (id)
);

CREATE TABLE own_titles (
    own_code int,
    own_title varchar(80),
    PRIMARY KEY (own_code)
);

CREATE TABLE industry_titles(
    industry_code varchar(10),
    industry_title varchar(200),
    PRIMARY KEY (industry_code)
);

CREATE TABLE agglvl_titles (
    agglvl_code int,
    agglvl_title varchar(80),
    PRIMARY KEY (agglvl_code)
);