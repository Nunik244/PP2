-- 1. Procedure to add a phone number to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone_number, phone_type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

-- 2. Procedure to move contact to group (creates group if missing)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
    v_contact_id INTEGER;
BEGIN
    -- Ensure the group exists and get its ID
    INSERT INTO groups (group_name)
    VALUES (p_group_name)
    ON CONFLICT (group_name) DO NOTHING;
    
    SELECT id INTO v_group_id FROM groups WHERE group_name = p_group_name;

    -- Update the contact
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;
    
    IF v_contact_id IS NOT NULL THEN
        UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
    ELSE
        RAISE NOTICE 'Contact % not found', p_contact_name;
    END IF;
END;
$$;

-- 3. Function to search contacts by pattern (name, email, or phones)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    username VARCHAR,
    email VARCHAR,
    phone_numbers TEXT
) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.username, 
        c.email, 
        string_agg(p.phone_number, ', ') -- Combine multiple phones into one string
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.username ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone_number ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.username, c.email;
END;
$$;