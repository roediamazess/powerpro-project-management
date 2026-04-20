-- =============================================================================
-- THE POWERPRO DATABASE SCHEMA (v2.1 FINAL)
-- Standards: UUID v4, 1NF Normalized, Soft Delete, System Audit Logs, WIB TZ
-- =============================================================================

-- Extension for UUID Generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- MODULE 0: SYSTEM & AUDIT
-- =============================================================================

CREATE TABLE "system_audit_logs" (
  "log_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "table_name" varchar(100) NOT NULL,
  "record_id" uuid NOT NULL,
  "action" varchar(20) NOT NULL, -- INSERT, UPDATE, DELETE
  "old_payload" jsonb,
  "new_payload" jsonb,
  "user_id" uuid,
  "ip_address" varchar(45),
  "user_agent" text,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- MODULE 1: AUTH & RBAC
-- =============================================================================

CREATE TABLE "roles" (
  "role_id" varchar(50) PRIMARY KEY, -- e.g., 'ADMIN', 'MANAGER', 'OFFICER'
  "name" varchar(100) NOT NULL,
  "description" text,
  "is_active" boolean DEFAULT true,
  "listindex" integer DEFAULT 0,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" boolean DEFAULT false,
  "deleted_at" timestamptz
);

CREATE TABLE "tiers" (
  "tier_id" varchar(50) PRIMARY KEY, -- e.g., 'T1', 'T2', 'T3'
  "name" varchar(100) NOT NULL,
  "is_active" boolean DEFAULT true,
  "listindex" integer DEFAULT 0,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" boolean DEFAULT false,
  "deleted_at" timestamptz
);

CREATE TABLE "users" (
  "user_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "username" varchar(50) UNIQUE NOT NULL,
  "password_hash" varchar(255) NOT NULL,
  "fullname" varchar(100) NOT NULL,
  "email" varchar(100) UNIQUE NOT NULL,
  "role_id" varchar(50) REFERENCES "roles"("role_id"),
  "tier_id" varchar(50) REFERENCES "tiers"("tier_id"),
  "start_work" date,
  "birthday" date,
  "is_active" boolean DEFAULT true,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "created_by" uuid REFERENCES "users"("user_id"),
  "updated_by" uuid REFERENCES "users"("user_id"),
  "is_deleted" boolean DEFAULT false,
  "deleted_at" timestamptz
);

-- =============================================================================
-- MODULE 2: CRM / PARTNER MANAGEMENT
-- =============================================================================

-- Master Lookups
CREATE TABLE "partner_types" ( "type_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer, "is_active" boolean DEFAULT true );
CREATE TABLE "partner_statuses" ( "status_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer, "is_active" boolean DEFAULT true );
CREATE TABLE "partner_groups" ( "group_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer, "is_active" boolean DEFAULT true );
CREATE TABLE "partner_areas" ( "area_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer, "is_active" boolean DEFAULT true );
CREATE TABLE "partner_sub_areas" ( 
  "sub_area_id" varchar(50) PRIMARY KEY, 
  "name" varchar(100), 
  "area_id" varchar(50) REFERENCES "partner_areas"("area_id"),
  "listindex" integer, 
  "is_active" boolean DEFAULT true 
);
CREATE TABLE "partner_system_versions" ( "version_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer, "is_active" boolean DEFAULT true );
CREATE TABLE "partner_implementation_types" ( "imp_type_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer, "is_active" boolean DEFAULT true );

CREATE TABLE "partners" (
  "partner_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "partner_cnc" varchar(20),
  "name" varchar(150) NOT NULL,
  "type_id" varchar(50) REFERENCES "partner_types"("type_id"),
  "status_id" varchar(50) REFERENCES "partner_statuses"("status_id"),
  "stars" integer,
  "rooms" integer,
  "outlets" integer,
  "version_id" varchar(50) REFERENCES "partner_system_versions"("version_id"),
  "system_live_at" timestamptz,
  "imp_type_id" varchar(50) REFERENCES "partner_implementation_types"("imp_type_id"),
  "group_id" varchar(50) REFERENCES "partner_groups"("group_id"),
  "address" text,
  "area_id" varchar(50) REFERENCES "partner_areas"("area_id"),
  "sub_area_id" varchar(50) REFERENCES "partner_sub_areas"("sub_area_id"),
  "last_visit_at" timestamptz,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "created_by" uuid REFERENCES "users"("user_id"),
  "updated_by" uuid REFERENCES "users"("user_id"),
  "is_deleted" boolean DEFAULT false,
  "deleted_at" timestamptz
);

CREATE TABLE "partner_contacts" (
  "contact_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "partner_id" uuid REFERENCES "partners"("partner_id") ON DELETE RESTRICT,
  "contact_name" varchar(100) NOT NULL,
  "position" varchar(100),
  "email" varchar(100),
  "phone" varchar(50),
  "is_primary" boolean DEFAULT false,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" boolean DEFAULT false
);

-- =============================================================================
-- MODULE 3: PROJECT MANAGEMENT
-- =============================================================================

CREATE TABLE "project_types" ( "type_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer );
CREATE TABLE "project_statuses" ( "status_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer );
CREATE TABLE "project_arrangements" ( "arrangement_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer );
CREATE TABLE "project_assignments" ( "assignment_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer );

CREATE TABLE "projects" (
  "project_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "cnc_id" varchar(20),
  "name" varchar(200) NOT NULL,
  "partner_id" uuid NOT NULL REFERENCES "partners"("partner_id") ON DELETE RESTRICT,
  "type_id" varchar(50) REFERENCES "project_types"("type_id"),
  "status_id" varchar(50) REFERENCES "project_statuses"("status_id"),
  "arrangement_id" varchar(50) REFERENCES "project_arrangements"("arrangement_id"),
  "assignment_id" varchar(50) REFERENCES "project_assignments"("assignment_id"),
  "start_date" timestamptz,
  "end_date" timestamptz,
  "total_days" integer,
  "point_ach" decimal(10,2),
  "point_req" decimal(10,2),
  "point_percent" decimal(5,2),
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "created_by" uuid REFERENCES "users"("user_id"),
  "updated_by" uuid REFERENCES "users"("user_id"),
  "is_deleted" boolean DEFAULT false,
  "deleted_at" timestamptz
);

-- Junction table for multiple PICs
CREATE TABLE "project_pics" (
  "project_id" uuid REFERENCES "projects"("project_id") ON DELETE RESTRICT,
  "user_id" uuid REFERENCES "users"("user_id") ON DELETE RESTRICT,
  "pic_role" varchar(50), -- e.g., 'LEADER', 'STAFF'
  "assigned_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "is_active" boolean DEFAULT true,
  PRIMARY KEY ("project_id", "user_id")
);

-- =============================================================================
-- MODULE 4: TASKS & TIMEBOXING
-- =============================================================================

CREATE TABLE "task_priorities" ( "priority_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer );
CREATE TABLE "task_statuses" ( "status_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer );
CREATE TABLE "task_departments" ( "dept_id" varchar(50) PRIMARY KEY, "name" varchar(100), "listindex" integer );

CREATE TABLE "tasks" (
  "task_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "task_no" varchar(20),
  "project_id" uuid REFERENCES "projects"("project_id"),
  "partner_id" uuid REFERENCES "partners"("partner_id"),
  "priority_id" varchar(50) REFERENCES "task_priorities"("priority_id"),
  "status_id" varchar(50) REFERENCES "task_statuses"("status_id"),
  "dept_id" varchar(50) REFERENCES "task_departments"("dept_id"),
  "assignee_id" uuid REFERENCES "users"("user_id"),
  "description" text,
  "action_solution" text,
  "start_date" timestamptz,
  "end_date" timestamptz,
  "due_date" timestamptz,
  "duration_minutes" integer,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "created_by" uuid REFERENCES "users"("user_id"),
  "updated_by" uuid REFERENCES "users"("user_id"),
  "is_deleted" boolean DEFAULT false,
  "deleted_at" timestamptz
);

-- =============================================================================
-- MODULE 5: COMPLIANCE SYSTEM (UUID Standard)
-- =============================================================================

CREATE TABLE "compliance_forms" (
  "form_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "form_code" varchar(20) UNIQUE NOT NULL,
  "name" varchar(150) NOT NULL,
  "form_type" varchar(10), -- e.g., 'HSE', 'TECH'
  "item_count" integer DEFAULT 0,
  "is_active" boolean DEFAULT true,
  "listindex" integer DEFAULT 0,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "created_by" uuid REFERENCES "users"("user_id"),
  "updated_by" uuid REFERENCES "users"("user_id"),
  "is_deleted" boolean DEFAULT false
);

CREATE TABLE "compliance_items" (
  "item_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "item_code" varchar(20) UNIQUE,
  "name" varchar(255) NOT NULL,
  "category" varchar(50), -- Industrial/Modbus Context
  "modbus_addr" varchar(50), -- [Optional] For IoT integration
  "is_active" boolean DEFAULT true,
  "listindex" integer DEFAULT 0,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "created_by" uuid REFERENCES "users"("user_id"),
  "updated_by" uuid REFERENCES "users"("user_id"),
  "is_deleted" boolean DEFAULT false
);

-- Junction for Forms and Items
CREATE TABLE "compliance_form_items" (
  "form_id" uuid REFERENCES "compliance_forms"("form_id") ON DELETE RESTRICT,
  "item_id" uuid REFERENCES "compliance_items"("item_id") ON DELETE RESTRICT,
  "listindex" integer DEFAULT 0,
  PRIMARY KEY ("form_id", "item_id")
);

CREATE TABLE "compliance_entries" (
  "entry_id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  "form_id" uuid REFERENCES "compliance_forms"("form_id"),
  "partner_id" uuid REFERENCES "partners"("partner_id"),
  "project_id" uuid REFERENCES "projects"("project_id"),
  "agent_id" uuid REFERENCES "users"("user_id"),
  "audit_phase" varchar(20), -- REGULAR, BEFORE, AFTER
  "baseline_id" uuid REFERENCES "compliance_entries"("entry_id"),
  "status" varchar(20), -- DRAFT, SUBMITTED, VERIFIED
  "location" varchar(100),
  "score_total" decimal(10,2),
  "score_max" decimal(10,2),
  "compliance_percent" decimal(5,2),
  "actual_date" timestamptz,
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  "created_by" uuid REFERENCES "users"("user_id"),
  "updated_by" uuid REFERENCES "users"("user_id"),
  "is_deleted" boolean DEFAULT false
);

CREATE TABLE "compliance_entry_scores" (
  "entry_id" uuid REFERENCES "compliance_entries"("entry_id") ON DELETE RESTRICT,
  "item_id" uuid REFERENCES "compliance_items"("item_id") ON DELETE RESTRICT,
  "score" integer,
  "remark" text,
  "photo_url" text, -- Link to AWS S3
  "created_at" timestamptz DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("entry_id", "item_id")
);

-- =============================================================================
-- INDEXES FOR PERFORMANCE (AG GRID OPTIMIZATION)
-- =============================================================================

CREATE INDEX "idx_partners_name" ON "partners" ("name");
CREATE INDEX "idx_projects_partner" ON "projects" ("partner_id");
CREATE INDEX "idx_tasks_assignee" ON "tasks" ("assignee_id");
CREATE INDEX "idx_tasks_status" ON "tasks" ("status_id");
CREATE INDEX "idx_compliance_entries_partner" ON "compliance_entries" ("partner_id");
CREATE INDEX "idx_audit_logs_record" ON "system_audit_logs" ("record_id");
