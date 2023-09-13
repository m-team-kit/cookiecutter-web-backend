BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> d149d20b44e4

CREATE TABLE template (
    id UUID NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    modified TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    "repoFile" VARCHAR NOT NULL, 
    title VARCHAR NOT NULL, 
    summary VARCHAR NOT NULL, 
    language VARCHAR NOT NULL, 
    picture VARCHAR NOT NULL, 
    "gitLink" VARCHAR NOT NULL, 
    "gitCheckout" VARCHAR NOT NULL, 
    score FLOAT, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_template_id ON template (id);

CREATE INDEX ix_template_language ON template (language);

CREATE INDEX "ix_template_repoFile" ON template ("repoFile");

CREATE TABLE "user" (
    subject VARCHAR NOT NULL, 
    issuer VARCHAR NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    modified TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    CONSTRAINT id PRIMARY KEY (subject, issuer)
);

CREATE INDEX ix_user_issuer ON "user" (issuer);

CREATE INDEX ix_user_subject ON "user" (subject);

CREATE TABLE score (
    id UUID NOT NULL, 
    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    modified TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    parent_id UUID NOT NULL, 
    value FLOAT NOT NULL, 
    owner_subject VARCHAR NOT NULL, 
    owner_issuer VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(owner_subject, owner_issuer) REFERENCES "user" (subject, issuer) ON DELETE CASCADE, 
    FOREIGN KEY(parent_id) REFERENCES template (id) ON DELETE CASCADE
);

CREATE INDEX ix_score_id ON score (id);

CREATE TABLE tag (
    id UUID NOT NULL, 
    parent_id UUID NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(parent_id) REFERENCES template (id) ON DELETE CASCADE
);

CREATE INDEX ix_tag_id ON tag (id);

CREATE INDEX ix_tag_name ON tag (name);

INSERT INTO alembic_version (version_num) VALUES ('d149d20b44e4') RETURNING alembic_version.version_num;

COMMIT;

