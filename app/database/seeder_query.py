CREATE_SCHEMA_USER = """
CREATE SCHEMA IF NOT EXISTS "user";
"""

CREATE_SCHEMAS = [CREATE_SCHEMA_USER]

# -- ----------------------------------------------------------------------------
# --  TABLES
# -- --------

CREATE_TABLE_ROLES = """
CREATE TABLE IF NOT EXISTS "user".roles (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE,
	description TEXT NULL,
	is_active BOOLEAN DEFAULT true,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


CREATE_TABLE_PERMISSIONS = """
CREATE TABLE IF NOT EXISTS "user".permissions (
	id SERIAL PRIMARY KEY,
	resource VARCHAR(50) NOT NULL,
	action VARCHAR(50) NOT NULL,
	description TEXT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT permissions_resource_action_unique UNIQUE (resource, action),
	CONSTRAINT permissions_check CHECK (action IN ('create', 'read', 'update', 'delete'))
);

CREATE INDEX IF NOT EXISTS idx_permission_resource ON "user".permissions(resource);
CREATE INDEX IF NOT EXISTS idx_permission_action ON "user".permissions(action);
"""

CREATE_TABLE_ROLE_PERMISSIONS = """
CREATE TABLE IF NOT EXISTS "user".role_permissions (
	id SERIAL PRIMARY KEY,
    permission_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_role_permissions_role
        FOREIGN KEY (role_id)
        REFERENCES "user".roles(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_permissions_permission
        FOREIGN KEY (permission_id)
        REFERENCES "user".permissions(id)
        ON DELETE CASCADE    
);

CREATE INDEX IF NOT EXISTS idx_role_permissions_role_id ON "user".role_permissions(role_id);
CREATE INDEX IF NOT EXISTS idx_role_permissions_permission ON "user".role_permissions(permission_id);
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
	password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_employee_role
        FOREIGN KEY (role_id)
        REFERENCES "user".roles(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_employees_email ON "user".employees(email);    
CREATE INDEX IF NOT EXISTS idx_employees_role_id ON "user".employees(role_id);    
CREATE INDEX IF NOT EXISTS idx_employees_is_active ON "user".employees(is_active);    
"""


CREATE_TABLES = [
    CREATE_TABLE_ROLES,
    CREATE_TABLE_PERMISSIONS,
    CREATE_TABLE_ROLE_PERMISSIONS,
    CREATE_TABLE_EMPLOYEES,
]


# -- ----------------------------------------------------------------------------
# --  FUNCTIONS
# -- ----------------------------------------------------------------------------
