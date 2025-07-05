
# imports
from neo4j import GraphDatabase
from typing import List, Dict
import os
import logging

logger = logging.getLogger(__name__)

# Neo4j driver
driver = None


def initialize_neo4j_driver(neo4j_ip_port: str, neo4j_user: str, neo4j_password: str, log=False):
    """Initialize the Neo4j driver"""
    global driver
    logger.info("Initializing Neo4j driver...")
    logger.info("neo4j_ip_port: {}".format(neo4j_ip_port))
    logger.info("neo4j_user: {}".format(neo4j_user))
    logger.info("neo4j_password: {}".format(neo4j_password))
    driver = GraphDatabase.driver(neo4j_ip_port, auth=(neo4j_user, neo4j_password))
    logger.info("Neo4j driver initialized")
    # test connection
    try:
        driver.verify_connectivity()
        logger.info("Connected to Neo4j")
    except Exception as e:
        logger.error("Failed to connect to Neo4j: {}".format(e))
    return driver

# methods
def run_cypher(cypher_query: str, log=False):
    '''
    queries a neo4j database
    '''
    # initialize
    list_result = []
    message = "Health check passed"
    query = cypher_query.strip()

    # log
    if log:
        logger.info("running query: \n{}".format(cypher_query))

    # make sure have neo4j parameters
    if driver:
        # execute the query    
        try:
            # read only for driver < 5
            # with driver.session(config=SessionConfig(default_access_mode="READ")) as session:
            # read only for driver versino >=5
            with driver.session(default_access_mode="r") as session:        
                cypher_result = session.run(query)
                # Convert each record to a dictionary
                list_result = [record.data() for record in cypher_result]
            
        except Exception as e:
            message = str(e)
            # raise HTTPException(status_code=500, detail=str(e))

    else:
        message = 'Driver not initialized'

    # build the json
    result = {'data': list_result, 'message': message}

    # return
    return result

