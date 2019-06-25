gunicorn \
    --reload\
    --workers 4\
    --log-level DEBUG\
    fun_hosp_server:api
