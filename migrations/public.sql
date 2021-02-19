/*
 Navicat Premium Data Transfer

 Source Server         : my_12
 Source Server Type    : PostgreSQL
 Source Server Version : 120005
 Source Host           : 194.99.21.140:5433
 Source Catalog        : Emcd
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120005
 File Encoding         : 65001

 Date: 19/02/2021 20:50:06
*/

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS "public"."account";
CREATE TABLE "public"."account" (
  "user_id" int8 NOT NULL,
  "account_id" uuid,
  "username" text  NOT NULL,
  "create_datetime" timestamp(6),
  "modified_datetime" timestamp(6)
)
;

-- ----------------------------
-- Table structure for account_coin
-- ----------------------------
DROP TABLE IF EXISTS "public"."account_coin";
CREATE TABLE "public"."account_coin" (
  "id" SERIAL,
  "account_id" uuid NOT NULL,
  "coin_id" text NOT NULL,
  "address" text  ,
  "total_count" int4 NOT NULL,
  "active_count" int4 NOT NULL,
  "inactive_count" int4 NOT NULL,
  "dead_count" int4 NOT NULL,
  "total_hashrate" int8 NOT NULL,
  "total_hashrate1h" int8 NOT NULL,
  "total_hashrate24h" int8 NOT NULL,
  "last_update_datetime" timestamp(6) NOT NULL,
  "is_active" bool NOT NULL,
  "user_id" int8 NOT NULL
)
;

-- ----------------------------
-- Table structure for account_coin_notification
-- ----------------------------
DROP TABLE IF EXISTS "public"."account_coin_notification";
CREATE TABLE "public"."account_coin_notification" (
  "account_coin_id" int4 NOT NULL,
  "is_enabled" bool NOT NULL DEFAULT true
)
;

-- ----------------------------
-- Table structure for lang
-- ----------------------------
DROP TABLE IF EXISTS "public"."lang";
CREATE TABLE "public"."lang" (
  "id" int4 NOT NULL,
  "name" text  NOT NULL
)
;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "public"."user";
CREATE TABLE "public"."user" (
  "id" int8 NOT NULL,
  "lang_id" int4 NOT NULL,
  "created_datetime" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Table structure for worker_account_history
-- ----------------------------
DROP TABLE IF EXISTS "public"."worker_account_history";
CREATE TABLE "public"."worker_account_history" (
  "account_coin_id" int4 NOT NULL,
  "worker_id" text NOT NULL,
  "stored_datetime" timestamp(6) NOT NULL,
  "status_id" int4 NOT NULL,
  "hashrate" int8 NOT NULL,
  "hashrate1h" int8 NOT NULL,
  "hashrate24h" int8 NOT NULL,
  "reject" float8 NOT NULL
)
;

-- ----------------------------
-- Function structure for generate_dataclass
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."generate_dataclass"(text, bool);

CREATE OR REPLACE FUNCTION "public"."generate_dataclass"(text, bool)
  RETURNS TABLE("table_name_generated" text, "declaration_generated" text) AS $BODY$
DECLARE
		select_start_def text default '';
		select_end_def text default '';

		property_def text default '';

		import_def text default 'import datetime'||chr(10)||'import typing'||chr(10)||'from dataclasses import dataclass'||chr(10)||chr(10);
		full_def text default chr(10);
		class_def text default '';
		column_def text default '';
    schema_name_ ALIAS FOR $1;
		separate_table alias for $2;
		table_ RECORD;
		column_ RECORD;
		name_part TEXT;
		t_name TEXT;
		is_first_column BOOLEAN DEFAULT true;
		t_name_array TEXT[];
		tables_ CURSOR (sc_name text) FOR SELECT table_name FROM information_schema.tables WHERE table_schema = sc_name;
		columns_ CURSOR (t_name text) FOR SELECT column_name, data_type, is_nullable from INFORMATION_SCHEMA.COLUMNS where table_name = t_name;
BEGIN
		open tables_(schema_name_);

		LOOP
				FETCH tables_ INTO table_;
				EXIT WHEN NOT FOUND;
				t_name := '';

				select into t_name_array regexp_split_to_array(table_.table_name, '_');

				foreach name_part in array t_name_array loop
						t_name := t_name || upper(substring(name_part from 1 for 1)) || substring(name_part from 2);

				end loop;

				class_def = '';
				--test := test || table_.table_name;
				class_def := '@dataclass'|| chr(10) ||'class ' || t_name || ':' || chr(10);
				
				select_start_def := chr(9) || '__select__ = """ select ';
				select_end_def := ' from ' || TABLE_.table_name || '"""' || chr(10);
				
				is_first_column := true;

				class_def := class_def;
				property_def := '';
				open columns_(table_.table_name);
				LOOP
					FETCH columns_ INTO column_;
					EXIT WHEN NOT FOUND;
					
					if is_first_column = false then 
						select_start_def := select_start_def ||  ', "' || COLUMN_.column_name || '"';
					ELSE
						select_start_def := select_start_def || '"' || COLUMN_.column_name || '"';
					end if;

					is_first_column := false;

					select
						case 
							when column_.data_type = 'uuid' then COLUMN_.column_name  || ': ' || case when column_.is_nullable = 'YES' then 'typing.Optional['||'UUID'||']' else 'UUID' end
							when column_.data_type = 'bigint' then COLUMN_.column_name || ': ' || case when column_.is_nullable = 'YES' then 'typing.Optional['||'int'||']' else 'int' end
							when column_.data_type = 'integer' then COLUMN_.column_name || ': ' || case when column_.is_nullable = 'YES' then 'typing.Optional['||'int'||']' else 'int' end
							when column_.data_type = 'timestamp without time zone' then COLUMN_.column_name || ': ' || case when column_.is_nullable = 'YES' then 'typing.Optional['||'datetime.datetime'||']' else 'datetime.datetime' end
							when column_.data_type = 'boolean' then COLUMN_.column_name || ': ' || case when column_.is_nullable = 'YES' then 'typing.Optional['||'bool'||']' else 'bool' end
							when column_.data_type = 'text' then COLUMN_.column_name || ': ' || case when column_.is_nullable = 'YES' then 'typing.Optional['||'str'||']' else 'str' end
							else COLUMN_.column_name || ': ' || case when column_.is_nullable = 'YES' then 'typing.Optional['||'typing.Any'||']' else 'typing.Any' end
						end as cn
					into column_def;
					raise notice '%', column_def;
					property_def := property_def || chr(9) || column_def || chr(10);
					
	
				END LOOP;

				class_def := class_def || property_def || chr(10) || select_start_def || select_end_def;

				close columns_;
				raise notice E'%', class_def;
				full_def := full_def || class_def || chr(10);
				if separate_table = TRUE THEN
					return query select t_name as table_name_generated, CONCAT(import_def, full_def) as declaration_generated;
					full_def := chr(10);
				end if;
		END LOOP;

		close tables_;
		raise notice '%', import_def||full_def;
		if separate_table = FALSE THEN
			return query select 'FullDump' as table_name_generated, CONCAT(import_def, full_def) as declaration_generated;
		end if;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."account_coin_id_seq"
OWNED BY "public"."account_coin"."id";
SELECT setval('"public"."account_coin_id_seq"', 25, true);

-- ----------------------------
-- Primary Key structure for table account
-- ----------------------------
ALTER TABLE "public"."account" ADD CONSTRAINT "account_pkey" PRIMARY KEY ("user_id");

-- ----------------------------
-- Primary Key structure for table account_coin
-- ----------------------------
ALTER TABLE "public"."account_coin" ADD CONSTRAINT "account_coin_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table account_coin_notification
-- ----------------------------
ALTER TABLE "public"."account_coin_notification" ADD CONSTRAINT "account_coin_notification_pkey" PRIMARY KEY ("account_coin_id");

-- ----------------------------
-- Primary Key structure for table lang
-- ----------------------------
ALTER TABLE "public"."lang" ADD CONSTRAINT "lang_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user
-- ----------------------------
ALTER TABLE "public"."user" ADD CONSTRAINT "user_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table worker_account_history
-- ----------------------------
ALTER TABLE "public"."worker_account_history" ADD CONSTRAINT "worker_account_history_pkey" PRIMARY KEY ("account_coin_id", "worker_id", "stored_datetime");

-- ----------------------------
-- Foreign Keys structure for table account
-- ----------------------------
ALTER TABLE "public"."account" ADD CONSTRAINT "account_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
