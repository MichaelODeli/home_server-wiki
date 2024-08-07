create table
  "users" (
    "id" serial primary key,
    "username" varchar(70) not null,
    "email" varchar(150) not null,
    "password" varchar(64) not null,
    "active" BOOLEAN DEFAULT TRUE,
    "admin_access" BOOLEAN DEFAULT FALSE,
    "created_at" timestamp not null default NOW(),
    "updated_at" timestamp not null default NOW(),
    UNIQUE(email),
    UNIQUE(username)
);

create table
  "config" (
    "id" serial primary key,
    "parameter_name" varchar(50) not null,
    "parameter_value" varchar(255),
    "test_value" BOOLEAN DEFAULT FALSE,
    "created_at" timestamp not null default NOW(),
    "updated_at" timestamp not null default NOW()
);

create table
  "mime_types_primary" (
    "id" serial primary key,
    "type_name" varchar(100) not null,
    "search_enabled" BOOLEAN not null DEFAULT TRUE,
    "created_at" timestamp not null default NOW(),
    "updated_at" timestamp not null default NOW()
);

create table
  "mime_types_secondary" (
    "id" serial primary key,
    "primary_mime_id" int not null,
    "type_name" varchar(100) not null,
    "extension" varchar(100),
    "compressible" BOOLEAN,
    "is_audio" BOOLEAN not null DEFAULT FALSE,
    "is_video" BOOLEAN not null DEFAULT FALSE,
    "html_video_ready" BOOLEAN not null DEFAULT FALSE,
    "html_audio_ready" BOOLEAN not null DEFAULT FALSE,
    "search_enabled" BOOLEAN not null DEFAULT TRUE,
    "created_at" timestamp not null default NOW(),
    "updated_at" timestamp not null default NOW(),
    FOREIGN KEY (primary_mime_id) REFERENCES mime_types_primary (id) ON DELETE CASCADE,
    UNIQUE(type_name)
);

create table
  "filestorage_categories" (
    "id" serial primary key,
    "category_name" varchar(50) not null,
    "category_pseudonym" varchar(50),
    "way" text not null,
    "is_absolute_way" BOOLEAN  not null DEFAULT FALSE,
    "main_mime_type_id" int,
    "search_enabled" BOOLEAN not null DEFAULT TRUE,
    "active" BOOLEAN DEFAULT TRUE,
    "created_at" timestamp not null default NOW(),
    "updated_at" timestamp not null default NOW(),
    FOREIGN KEY (main_mime_type_id) REFERENCES mime_types_primary (id) ON DELETE CASCADE,
    UNIQUE(category_name)
);

create table
  "filestorage_types" (
    "id" serial primary key,
    "category_id" int not null,
    "type_name" varchar(50) not null,
    "type_pseudonym" varchar(50),
    "way" text not null,
    "is_absolute_way" BOOLEAN not null DEFAULT FALSE,
    "main_mime_type_id" int,
    "search_enabled" BOOLEAN not null DEFAULT TRUE,
    "active" BOOLEAN DEFAULT TRUE,
    "created_at" timestamp not null default NOW(),
    "updated_at" timestamp not null default NOW(),
    FOREIGN KEY (category_id) REFERENCES filestorage_categories (id) ON DELETE CASCADE,
    FOREIGN KEY (main_mime_type_id) REFERENCES mime_types_primary (id) ON DELETE CASCADE,
    UNIQUE(category_id, type_name)
);

create table
  "filestorage_files" (
    "id" uuid not null primary key,
    "type_id" int not null,
    "way" text not null DEFAULT '/',
    "filename" text not null,
    "is_absolute_way" BOOLEAN not null DEFAULT FALSE,
    "mime_type_id" int not null,
    "size_kb" int not null DEFAULT 0,
    "created_at" timestamp not null default NOW(),
    "updated_at" timestamp not null default NOW(),
    FOREIGN KEY (type_id) REFERENCES filestorage_types (id) ON DELETE CASCADE,
    FOREIGN KEY (mime_type_id) REFERENCES mime_types_secondary (id) ON DELETE CASCADE,
    UNIQUE(id, type_id)
);

create table
  "filestorage_mediainfo" (
    "id" serial primary key,
    "file_id" uuid not null,
    "duration" real not null,
    "fps" int,
    "codec" varchar(20),
    "created_at" timestamp not null default NOW(),
    "updated_at" timestamp not null default NOW(),
    FOREIGN KEY (file_id) REFERENCES filestorage_files (id) ON DELETE CASCADE
);
