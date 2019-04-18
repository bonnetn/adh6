class RubyHashTrackable:
    """
    Define a class on which you can record modification and get the result as
    ruby/hash modification (like ADH5 does).

    Override this function if you want to add information (for instance the
    adherent linked to the modification, since this function will always return
    None.)
    """

    def take_snapshot(self) -> dict:
        """
        Converts a SQLAlchemy row to a dictionnary of Column:Value
        """
        return dict((column.name, getattr(self, column.name))
                    for column in self.__table__.columns)

    def get_related_member(self):
        raise NotImplemented()

    def serialize_snapshot_diff(self, snap_before, snap_after) -> str:
        raise NotImplemented()
