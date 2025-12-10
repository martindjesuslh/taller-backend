# -- ----------------------------------------------------------------------------
# --  CONFIG
# -- ----------------------------------------------------------------------------

CONFIGURE_TIMEZONE = """
SET timezone = 'UTC';
"""

CREATE_CONFIGS = [CONFIGURE_TIMEZONE]

# -- ----------------------------------------------------------------------------
# --  SCHEMAS
# -- ----------------------------------------------------------------------------


CREATE_SCHEMA_PUBLIC = """
CREATE SCHEMA IF NOT EXISTS "public";
"""

CREATE_SCHEMA_USER = """
CREATE SCHEMA IF NOT EXISTS "user";
"""

CREATE_SCHEMAS = [CREATE_SCHEMA_PUBLIC, CREATE_SCHEMA_USER]

# -- ----------------------------------------------------------------------------
# --  TABLES
# -- --------

CREATE_TABLE_ROLES = """
CREATE TABLE IF NOT EXISTS "user".roles (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	description TEXT NULL,
	is_active BOOLEAN DEFAULT true,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NOW()
);
"""


CREATE_TABLE_PERMISSIONS = """
CREATE TABLE IF NOT EXISTS "user".permissions (
	id SERIAL PRIMARY KEY,
	resource VARCHAR(50) NOT NULL,
	action VARCHAR(50) NOT NULL,
	description TEXT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
	CONSTRAINT permissions_resource_action_unique UNIQUE (resource, action),
	CONSTRAINT permissions_check CHECK (action IN ('create', 'read', 'update', 'delete'))
);
"""

CREATE_TABLE_ROLE_PERMISSIONS = """
CREATE TABLE IF NOT EXISTS "user".role_permissions (
	id SERIAL PRIMARY KEY,
    permission_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_role_permissions_role
        FOREIGN KEY (role_id)
        REFERENCES "user".roles(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_permissions_permission
        FOREIGN KEY (permission_id)
        REFERENCES "user".permissions(id)
        ON DELETE CASCADE    
);
"""

CREATE_TABLE_EMPLOYEES = """
CREATE TABLE IF NOT EXISTS "user".employees (
	id SERIAL PRIMARY KEY,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	email VARCHAR(150) NOT NULL UNIQUE,
	phone VARCHAR(20) NULL,
	address TEXT,
	is_active BOOL DEFAULT true,
	password VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT fk_employee_role
        FOREIGN KEY (role_id)
        REFERENCES "user".roles(id)
        ON DELETE CASCADE
);    
"""


CREATE_TABLES = [
    CREATE_TABLE_ROLES,
    CREATE_TABLE_PERMISSIONS,
    CREATE_TABLE_ROLE_PERMISSIONS,
    CREATE_TABLE_EMPLOYEES,
]


# -- ----------------------------------------------------------------------------
# --  INDEX
# -- ----------------------------------------------------------------------------

CREATE_INDEXES_PERMISSIONS = """
CREATE INDEX IF NOT EXISTS idx_permission_resource ON "user".permissions(resource);
CREATE INDEX IF NOT EXISTS idx_permission_action ON "user".permissions(action);
"""

CREATE_INDEXES_ROLE_PERMISSIONS = """
CREATE INDEX IF NOT EXISTS idx_role_permissions_role_id ON "user".role_permissions(role_id);
CREATE INDEX IF NOT EXISTS idx_role_permissions_permission ON "user".role_permissions(permission_id);
"""

CREATE_INDEXES_EMPLOYEES = """
CREATE INDEX IF NOT EXISTS idx_employees_email ON "user".employees(email);    
CREATE INDEX IF NOT EXISTS idx_employees_role_id ON "user".employees(role_id);    
CREATE INDEX IF NOT EXISTS idx_employees_is_active ON "user".employees(is_active);
"""

CREATE_INDEXES = [
    CREATE_INDEXES_PERMISSIONS,
    CREATE_INDEXES_ROLE_PERMISSIONS,
    CREATE_INDEXES_EMPLOYEES,
]

# -- ----------------------------------------------------------------------------
# --  FUNCTIONS
# -- ----------------------------------------------------------------------------

CREATE_FUNCTION_UPDATE_UPDATED_AT_COLUMN = """
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

CREATE_FUNCTIONS = [CREATE_FUNCTION_UPDATE_UPDATED_AT_COLUMN]


# -- ----------------------------------------------------------------------------
# --  TRIGGERS
# -- ----------------------------------------------------------------------------


def trigger_update_updated_column(schema: str, table: str):
    return f"""
DROP TRIGGER IF EXISTS trigger_{table}_updated_at ON "{schema}".{table};
CREATE TRIGGER trigger_{table}_updated_at
    BEFORE UPDATE ON "{schema}".{table}
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();
"""


CREATE_TRIGGER_UPDATE_UPDATED_COLUMN_ROLES = trigger_update_updated_column(
    "user", "roles"
)
CREATE_TRIGGER_UPDATE_UPDATED_COLUMN_PERMISSIONS = trigger_update_updated_column(
    "user", "permissions"
)
CREATE_TRIGGER_UPDATE_UPDATED_COLUMN_ROLE_PERMISSIONS = trigger_update_updated_column(
    "user", "role_permissions"
)
CREATE_TRIGGER_UPDATE_UPDATED_COLUMN_EMPLOYEES = trigger_update_updated_column(
    "user", "employees"
)

CREATE_TRIGGERS = [
    CREATE_TRIGGER_UPDATE_UPDATED_COLUMN_ROLES,
    CREATE_TRIGGER_UPDATE_UPDATED_COLUMN_PERMISSIONS,
    CREATE_TRIGGER_UPDATE_UPDATED_COLUMN_ROLE_PERMISSIONS,
    CREATE_TRIGGER_UPDATE_UPDATED_COLUMN_EMPLOYEES,
]
