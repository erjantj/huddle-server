#!/usr/bin/env python3
import os
from flaskr import celery, create_app

app = create_app()
app.app_context().push()