gunicorn \
    --reload\
    --workers 1\
    --log-level DEBUG\
    fun_hosp_server:api
