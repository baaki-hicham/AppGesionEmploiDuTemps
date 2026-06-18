from extensions import db


class EntityController:
    def __init__(self, model):
        self.model = model

    def list_all(self):
        return self.model.query.order_by(self.model.id.desc()).all()

    def paginate(self, page=1, per_page=10, query=None):
        query = query or self.model.query
        return query.order_by(self.model.id.desc()).paginate(page=page, per_page=per_page, error_out=False)

    def get_by_id(self, entity_id):
        return self.model.query.get(entity_id)

    def create(self, **data):
        entity = self.model(**data)
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity, **data):
        for field, value in data.items():
            setattr(entity, field, value)
        db.session.commit()
        return entity

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
        return True
