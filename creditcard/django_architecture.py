from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.generic.network import Firewall

with Diagram("Django System Architecture", show=True, filename="django_architecture", outformat="png"):

    user = User("User")

    with Cluster("Django Backend"):
        backend = Server("Django Server")

        with Cluster("Apps"):
            fraud_app = Python("Fraud App")

        with Cluster("Machine Learning Models"):
            ml_models = [Storage("Isolation Forest"), Storage("Logistic Regression"), Storage("Scaler")]

    with Cluster("Database"):
        db = PostgreSQL("SQLite DB")

    with Cluster("Static & Templates"):
        static_files = Storage("Static Files (CSS, JS, Images)")
        templates = Storage("HTML Templates")

    with Cluster("Security"):
        firewall = Firewall("Django Security Middleware")

    user >> firewall >> backend >> db
    backend >> fraud_app >> ml_models
    backend >> static_files
    backend >> templates
