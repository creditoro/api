"""
This module is intended for common/shared functionality between ORM classes in the models dir.
"""
import logging
from uuid import UUID

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.extensions import DB

logger = logging.getLogger(__name__)


def commit():
    """
    Commits changes to the database, and catches DBAPIErrors.
    error)
    :return: (bool) True if operation was a success, otherwise False.
    """
    try:
        DB.session.commit()
        return True
    except (SQLAlchemyError, IntegrityError) as error:
        print(error)
        logger.debug("dbapierror: %s", error)
        DB.session.rollback()
        return False
    except Exception as exception:
        print(exception)
        logger.error("Unhandled exception: %s", exception)


class Base(DB.Model):
    """Meant to be used as a base class for all our "database-table" classes instead of db.Model."""
    __abstract__ = True

    def store(self):
        """
        Adds this object to the database session and tries to commit it.
        :return (bool) True if operation was successful otherwise False.
        """
        DB.session.add(self)
        return commit()

    def remove(self) -> bool:
        """
        Removes this object from the database and commits it (stores the changes).
        :return: (bool) True if the operation was successful, otherwise False.
        """
        DB.session.delete(self)
        if commit():
            return True
        return False

    def serialize(self):
        """
            Serializes the class by iterating over all it's variables and turns them into a
            dictionary.
            example usage: return jsonify({"result": YourClass.serialize()})
            :return (dict) self.
        """
        result = {}
        for key in inspect(self).attrs.keys():
            attribute = getattr(self, key)
            if isinstance(key, UUID):
                attribute = str(attribute)
            result.update({key: attribute})
        return result

    @staticmethod
    def serialize_list(list_to_serialize):
        """
        Serializes a list of self.
        example usage: return jsonify({"results": YourClass.serialize_list(data)})
        :return (list) of self as dict.
        """
        return [element.serialize() for element in list_to_serialize]
