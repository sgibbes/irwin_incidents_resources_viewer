
import test_query


def query_related_tables(inputs, token, sql):

    # query capability table

    response = test_query.query_api(inputs, token, sql)
    # capability_response = test_query.load_response(response)

    return response['features'][0]['attributes']
