CREATE TABLE "partner_type" (
  "type_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "partner_status" (
  "status_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "partner_system_version" (
  "system_version_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "partner_implementation_type" (
  "implementation_type_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "partner_group" (
  "group_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "partner_area" (
  "area_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "partner_sub_area" (
  "sub_area_id" varchar PRIMARY KEY,
  "name" varchar,
  "header_area" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "partners" (
  "partner_id" uuid PRIMARY KEY,
  "partner_cnc" varchar,
  "name" varchar,
  "type" varchar,
  "status" varchar,
  "stars" integer,
  "rooms" integer,
  "outlets" integer,
  "system_version" varchar,
  "system_live" timestamp,
  "implementation_type" varchar,
  "group_id" varchar,
  "address" text,
  "area" varchar,
  "sub_area" varchar,
  "last_visit" timestamp,
  "last_visit_type" varchar,
  "last_project" varchar,
  "last_project_type" varchar,
  "contact_gm" varchar,
  "email_gm" varchar,
  "contact_fc" varchar,
  "email_fc" varchar,
  "contact_ca" varchar,
  "email_ca" varchar,
  "contact_cc" varchar,
  "email_cc" varchar,
  "contact_ia" varchar,
  "email_ia" varchar,
  "contact_ar" varchar,
  "email_ar" varchar,
  "contact_ap" varchar,
  "email_ap" varchar,
  "contact_itm" varchar,
  "email_itm" varchar,
  "contact_it" varchar,
  "email_it" varchar,
  "contact_hr" varchar,
  "email_hr" varchar,
  "contact_fom" varchar,
  "email_fom" varchar,
  "contact_fospv" varchar,
  "email_fospv" varchar,
  "contact_smm" varchar,
  "email_smm" varchar,
  "contact_sm" varchar,
  "email_sm" varchar,
  "contact_hkm" varchar,
  "email_hkm" varchar,
  "contact_hkspv" varchar,
  "email_hkspv" varchar,
  "contact_fbm" varchar,
  "email_fbm" varchar,
  "contact_fb" varchar,
  "email_fb" varchar,
  "createdate" timestamp,
  "createuser" uuid,
  "editdate" timestamp,
  "edituser" uuid
);

CREATE TABLE "project_type" (
  "type_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "project_status" (
  "status_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "project_arrangement" (
  "arrangement_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "project_assignment" (
  "assignment_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "project_information" (
  "information_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "projects" (
  "project_id" uuid PRIMARY KEY,
  "cnc_id" varchar,
  "name" varchar,
  "pic" varchar,
  "arrangement" varchar,
  "assignment" varchar,
  "information" varchar,
  "type" varchar,
  "status" varchar,
  "partner_id" uuid,
  "partner_name" varchar,
  "start_date" timestamp,
  "end_date" timestamp,
  "total_days" integer,
  "handover_or" timestamp,
  "handover_days" integer,
  "pic_kpi_2" decimal,
  "point_ach" decimal,
  "point_req" decimal,
  "point_percent" decimal,
  "check_or" timestamp,
  "check_days" integer,
  "officer_kpi2" decimal,
  "validation_date" timestamp,
  "validation_days" integer,
  "okr_kpi2" decimal,
  "pic_email" varchar,
  "s1_estimation" timestamp,
  "s1_over_days" integer,
  "s1_count_email_sent" integer,
  "s2_email_sent" integer,
  "s3_email_sent" integer,
  "pyear" integer,
  "pquarter" integer,
  "pmonth" integer,
  "pweekno" integer,
  "pweekofmonth" integer,
  "createdate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "timeboxing_type" (
  "type_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "timeboxing_priority" (
  "priority_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "timeboxing_status" (
  "status_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "timeboxing" (
  "timeboxing_id" uuid PRIMARY KEY,
  "timeboxing_no" varchar,
  "cnc_no" varchar,
  "type" varchar,
  "priority" varchar,
  "status" varchar,
  "user_position" varchar,
  "partner_id" uuid,
  "partner_name" varchar,
  "project_id" uuid,
  "project_name" varchar,
  "description" text,
  "action_solution" text,
  "start_date" timestamp,
  "end_date" timestamp,
  "duration" integer,
  "due_date" timestamp,
  "createdate" timestamp,
  "createuser" uuid,
  "editdate" timestamp,
  "edituser" uuid,
  "completedate" timestamp,
  "completeuser" uuid
);

CREATE TABLE "tasks_priority" (
  "priority_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "tasks_department" (
  "department_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "tasks_application" (
  "application_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "tasks_type" (
  "type_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "tasks_status" (
  "status_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "cratedate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "tasks" (
  "tasks_id" uuid PRIMARY KEY,
  "tasks_no" varchar,
  "cnc_no" varchar,
  "priority" varchar,
  "department" varchar,
  "application" varchar,
  "type" varchar,
  "status" varchar,
  "user_position" varchar,
  "partner_id" uuid,
  "partner_name" varchar,
  "project_id" uuid,
  "project_name" varchar,
  "description" text,
  "action_solution" text,
  "action_solution_internal" text,
  "start_date" timestamp,
  "end_date" timestamp,
  "duration" integer,
  "due_date" timestamp,
  "createdate" timestamp,
  "createuser" uuid,
  "editdate" timestamp,
  "edituser" uuid,
  "completedate" timestamp,
  "completeuser" uuid
);

CREATE TABLE "compliance_form" (
  "form_id" integer PRIMARY KEY,
  "form_type" varchar(4),
  "form_code" varchar(16),
  "name" varchar(80),
  "compliance_note" varchar(40),
  "location_type" varchar(4),
  "item_count" smallint,
  "need_qty_count" smallint,
  "listindex" smallint,
  "inspection_last" timestamp,
  "inspection_counter" integer,
  "roomtype" varchar(8),
  "flag_active" boolean,
  "createdate" timestamp,
  "editdate" timestamp,
  "createuser" varchar(12),
  "edituser" varchar(12)
);

CREATE TABLE "compliance_item" (
  "item_id" integer PRIMARY KEY,
  "name" varchar(80),
  "compliance_note" varchar(40),
  "job_type" varchar(4),
  "area" varchar(4),
  "default_form_type" varchar(4),
  "listindex" smallint,
  "flag_active" boolean,
  "code" varchar(16),
  "tags" varchar(80),
  "createdate" timestamp,
  "editdate" timestamp,
  "createuser" varchar(12),
  "edituser" varchar(12),
  "job_counter" smallint,
  "flag_qty" boolean,
  "defa_qty" decimal,
  "fa_master_id" integer
);

CREATE TABLE "compliance_form_score" (
  "score_id" integer PRIMARY KEY,
  "form_type" varchar(4),
  "code" varchar(12),
  "name" varchar(40),
  "score" smallint,
  "listindex" smallint,
  "createdate" timestamp,
  "editdate" timestamp,
  "createuser" varchar(12),
  "edituser" varchar(12),
  "color" varchar(16),
  "icon" varchar(40)
);

CREATE TABLE "compliance_form_item" (
  "form_id" integer,
  "item_id" integer,
  "listindex" smallint,
  "flag_active" boolean,
  "createdate" timestamp,
  "createuser" varchar(12),
  PRIMARY KEY ("form_id", "item_id")
);

CREATE TABLE "compliance_entry" (
  "entry_id" integer PRIMARY KEY,
  "partner_id" uuid,
  "project_id" uuid,
  "audit_phase" varchar(15),
  "baseline_entry_id" integer,
  "form_id" integer,
  "schedule_date" date,
  "status" char(1),
  "location" varchar(80),
  "label" varchar(80),
  "compliance_note" varchar(40),
  "agent_id" varchar(12),
  "item_count" integer,
  "form_score_max" decimal,
  "entered_score" decimal,
  "entered_counter" integer,
  "photo_count" integer,
  "entry_mode" varchar(2),
  "createdate" timestamp,
  "editdate" timestamp,
  "createuser" varchar(12),
  "edituser" varchar(12),
  "date_start" timestamp,
  "date_end" timestamp,
  "missing_item_count" smallint,
  "missing_item_qty" decimal,
  "req_count" integer,
  "status_index" smallint,
  "pyear" integer,
  "pquarter" integer,
  "pmonth" smallint,
  "score_avg" decimal,
  "total_max_score" decimal,
  "compliance" decimal,
  "duration" integer,
  "actual_date" timestamp,
  "form_type" varchar(4)
);

CREATE TABLE "compliance_entry_score" (
  "entry_id" integer,
  "item_id" integer,
  "score_id" integer,
  "score" smallint,
  "remark" text,
  "defa_qty" decimal,
  "qty" decimal,
  "req_count" smallint,
  "createdate" timestamp,
  "createuser" varchar(12),
  "photo_count" smallint,
  "fa_master_id" integer,
  "location" varchar(16),
  "missing_qty" decimal,
  "form_id" integer,
  PRIMARY KEY ("entry_id", "item_id")
);

CREATE TABLE "roles" (
  "role_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "createdate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "tiers" (
  "tier_id" varchar PRIMARY KEY,
  "name" varchar,
  "flag_active" boolean,
  "listindex" integer,
  "createdate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

CREATE TABLE "users" (
  "user_id" uuid PRIMARY KEY,
  "username" varchar UNIQUE,
  "password_hash" varchar,
  "fullname" varchar,
  "email" varchar UNIQUE,
  "tier_id" varchar,
  "role_id" varchar,
  "start_work" date,
  "birthday" date,
  "flag_active" boolean,
  "createdate" timestamp,
  "editdate" timestamp,
  "createuser" uuid,
  "edituser" uuid
);

COMMENT ON COLUMN "timeboxing"."partner_name" IS 'Pertimbangkan untuk dihapus jika ingin normalisasi data penuh';

COMMENT ON COLUMN "timeboxing"."project_name" IS 'Pertimbangkan untuk dihapus jika ingin normalisasi data penuh';

COMMENT ON COLUMN "compliance_entry"."partner_id" IS 'Menghubungkan entri dengan klien hotel';

COMMENT ON COLUMN "compliance_entry"."project_id" IS 'Opsional: Jika terikat pada project perbaikan tertentu';

COMMENT ON COLUMN "compliance_entry"."audit_phase" IS 'Isi dengan: REGULAR, BEFORE, atau AFTER';

COMMENT ON COLUMN "compliance_entry"."baseline_entry_id" IS 'Jika ini form AFTER, isi dengan entry_id form BEFORE-nya';

COMMENT ON COLUMN "compliance_entry"."pyear" IS 'Tahun fiskal entri';

COMMENT ON COLUMN "compliance_entry"."pquarter" IS 'Kuartal entri (1-4)';

COMMENT ON COLUMN "compliance_entry"."pmonth" IS 'Bulan entri (1-12)';

COMMENT ON COLUMN "compliance_entry"."score_avg" IS 'Computed Field';

COMMENT ON COLUMN "compliance_entry"."total_max_score" IS 'Computed Field';

COMMENT ON COLUMN "compliance_entry"."compliance" IS 'Computed Field';

COMMENT ON COLUMN "compliance_entry"."duration" IS 'Computed Field';

COMMENT ON COLUMN "compliance_entry_score"."missing_qty" IS 'Computed: qty - defa_qty';

COMMENT ON COLUMN "roles"."role_id" IS 'Contoh: ADMIN, MGT, OFFICER, USER';

COMMENT ON COLUMN "roles"."name" IS 'Contoh: Administrator, Management, Admin Officer';

COMMENT ON COLUMN "tiers"."tier_id" IS 'Contoh: T_NEW, T_1, T_2, T_3, T_4';

COMMENT ON COLUMN "tiers"."name" IS 'Contoh: New Born, Tier 1, Tier 2';

COMMENT ON COLUMN "users"."password_hash" IS 'Wajib ada untuk login, simpan dalam bentuk hash (Bcrypt/Argon2)';

COMMENT ON COLUMN "users"."tier_id" IS 'Relasi ke tabel tiers';

COMMENT ON COLUMN "users"."role_id" IS 'Relasi ke tabel roles';

COMMENT ON COLUMN "users"."createuser" IS 'Self-referencing ke user_id';

COMMENT ON COLUMN "users"."edituser" IS 'Self-referencing ke user_id';

ALTER TABLE "partner_sub_area" ADD FOREIGN KEY ("header_area") REFERENCES "partner_area" ("area_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "partners" ADD FOREIGN KEY ("type") REFERENCES "partner_type" ("type_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "partners" ADD FOREIGN KEY ("status") REFERENCES "partner_status" ("status_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "partners" ADD FOREIGN KEY ("group_id") REFERENCES "partner_group" ("group_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "partners" ADD FOREIGN KEY ("system_version") REFERENCES "partner_system_version" ("system_version_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "partners" ADD FOREIGN KEY ("implementation_type") REFERENCES "partner_implementation_type" ("implementation_type_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "partners" ADD FOREIGN KEY ("area") REFERENCES "partner_area" ("area_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "partners" ADD FOREIGN KEY ("sub_area") REFERENCES "partner_sub_area" ("sub_area_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "projects" ADD FOREIGN KEY ("type") REFERENCES "project_type" ("type_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "projects" ADD FOREIGN KEY ("information") REFERENCES "project_information" ("information_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "projects" ADD FOREIGN KEY ("status") REFERENCES "project_status" ("status_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "projects" ADD FOREIGN KEY ("assignment") REFERENCES "project_assignment" ("assignment_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "projects" ADD FOREIGN KEY ("arrangement") REFERENCES "project_arrangement" ("arrangement_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "projects" ADD FOREIGN KEY ("partner_id") REFERENCES "partners" ("partner_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "timeboxing" ADD FOREIGN KEY ("type") REFERENCES "timeboxing_type" ("type_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "timeboxing" ADD FOREIGN KEY ("priority") REFERENCES "timeboxing_priority" ("priority_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "timeboxing" ADD FOREIGN KEY ("status") REFERENCES "timeboxing_status" ("status_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "timeboxing" ADD FOREIGN KEY ("partner_id") REFERENCES "partners" ("partner_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "timeboxing" ADD FOREIGN KEY ("project_id") REFERENCES "projects" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tasks" ADD FOREIGN KEY ("priority") REFERENCES "tasks_priority" ("priority_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tasks" ADD FOREIGN KEY ("department") REFERENCES "tasks_department" ("department_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tasks" ADD FOREIGN KEY ("application") REFERENCES "tasks_application" ("application_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tasks" ADD FOREIGN KEY ("type") REFERENCES "tasks_type" ("type_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tasks" ADD FOREIGN KEY ("status") REFERENCES "tasks_status" ("status_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tasks" ADD FOREIGN KEY ("project_id") REFERENCES "projects" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tasks" ADD FOREIGN KEY ("partner_id") REFERENCES "partners" ("partner_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_entry" ADD FOREIGN KEY ("partner_id") REFERENCES "partners" ("partner_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_entry" ADD FOREIGN KEY ("project_id") REFERENCES "projects" ("project_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_entry" ADD FOREIGN KEY ("baseline_entry_id") REFERENCES "compliance_entry" ("entry_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_form_item" ADD FOREIGN KEY ("form_id") REFERENCES "compliance_form" ("form_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_form_item" ADD FOREIGN KEY ("item_id") REFERENCES "compliance_item" ("item_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_entry" ADD FOREIGN KEY ("form_id") REFERENCES "compliance_form" ("form_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_entry_score" ADD FOREIGN KEY ("entry_id") REFERENCES "compliance_entry" ("entry_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_entry_score" ADD FOREIGN KEY ("item_id") REFERENCES "compliance_item" ("item_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "compliance_entry_score" ADD FOREIGN KEY ("score_id") REFERENCES "compliance_form_score" ("score_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "users" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("role_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "users" ADD FOREIGN KEY ("tier_id") REFERENCES "tiers" ("tier_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "users" ADD FOREIGN KEY ("createuser") REFERENCES "users" ("user_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "users" ADD FOREIGN KEY ("edituser") REFERENCES "users" ("user_id") DEFERRABLE INITIALLY IMMEDIATE;
