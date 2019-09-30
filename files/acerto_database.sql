DROP TABLE registers_registersaddress;

CREATE TABLE `registers_registersaddress` (
	`pk_registers_address`	integer NOT NULL PRIMARY KEY,
	`address`	varchar ( 100 ) NOT NULL,
	`number`	integer NOT NULL,
	`complement`	varchar ( 100 ),
	`quarter`	varchar ( 50 ) NOT NULL,
	`zip_code`	varchar ( 15 ) NOT NULL,
	`fk_cities_id`	varchar(10) NOT NULL,
	`fk_registers_id`	integer NOT NULL,
	FOREIGN KEY(`fk_registers_id`) REFERENCES `registers_registers`(`pk_registers`) DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY(`fk_cities_id`) REFERENCES `localization_cities`(`pk_cities`) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE `localization_states` (
	`pk_states`	varchar ( 5 ) NOT NULL,
	`name_state`	varchar ( 100 ) NOT NULL,
	`state_symbol`	varchar ( 2 ) NOT NULL,
	`time_zone`	varchar ( 50 ) NOT NULL,
	`fk_countries_id`	smallint NOT NULL,
	`kc_cities` integer not null,
	FOREIGN KEY(`fk_countries_id`) REFERENCES `localization_countries`(`pk_countries`) DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY(`pk_states`)
);

DROP TABLE localization_cities;

CREATE TABLE `localization_cities` (
	`pk_cities`	varchar(10) NOT NULL PRIMARY KEY,
	`name_city`	varchar ( 150 ) NOT NULL,
	`zip_code`	varchar ( 15 ) NOT NULL,
	`fk_states_id`	varchar(5) NOT NULL,
	FOREIGN KEY(`fk_states_id`) REFERENCES `localization_states`(`pk_states`) DEFERRABLE INITIALLY DEFERRED
);

drop table localization_provinces;

commit;

create table taxes_taxes (
    pk_taxes varchar(15) not null primary key,
    taxdef decimal(5,2) default 0.0 not null,
    fk_countries_destiny_id integer not null,
    fk_countries_origin_id integer not null,
    fk_states_destiny_id varchar(5) not null,
    fk_states_origin_id varchar(5) not null,
    fk_type_taxes_id integer not null,
	foreign key (fk_countries_destiny_id) REFERENCES localization_countries(pk_countries) DEFERRABLE INITIALLY DEFERRED,
	foreign key (fk_countries_origin_id) REFERENCES localization_countries(pk_countries) DEFERRABLE INITIALLY DEFERRED,
	foreign key (fk_states_destiny_id) REFERENCES localization_states(pk_states) DEFERRABLE INITIALLY DEFERRED,
	foreign key (fk_states_destiny_id) REFERENCES localization_states(pk_states) DEFERRABLE INITIALLY DEFERRED,
	foreign key (fk_type_taxes_id) REFERENCES taxesaux_typetaxes(pk_type_taxes) DEFERRABLE INITIALLY DEFERRED
);

create table taxes_ncmtaxes (
    pk_ncmtaxes integer not null primary key autoincrement,
    tax decimal(5,2) default 0.0,
    fk_ncmcodes_id varchar(15) not null,
	fk_taxes_id varchar(15) not null,
	foreign key (fk_ncmcodes_id) REFERENCES taxesaux_ncmcodes(pk_ncmcodes) DEFERRABLE INITIALLY DEFERRED,
	foreign key (fk_taxes_id) REFERENCES taxes_taxes(pk_taxes) DEFERRABLE INITIALLY DEFERRED
);

commit;
