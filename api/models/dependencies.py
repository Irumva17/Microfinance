from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta, date
from django.core.exceptions import ValidationError