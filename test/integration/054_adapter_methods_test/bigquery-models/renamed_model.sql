select * from {{ source('test_source', 'renamed_seed') }}
