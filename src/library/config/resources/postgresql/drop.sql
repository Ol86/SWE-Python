DROP INDEX IF EXISTS
    address_library_id_idx,
    address_postal_code_idx,
    book_member_id_idx,
    member_last_name_idx;

DROP TABLE IF EXISTS
    address,
    book,
    member;

DROP TYPE IF EXISTS
    gender,
    genre;
