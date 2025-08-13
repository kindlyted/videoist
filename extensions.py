from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate

# 初始化扩展实例（不包含具体配置）
db = SQLAlchemy()

mail = Mail()
migrate = Migrate()
