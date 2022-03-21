# This file is part of Zoom Autojoiner GUI.

# Zoom Autojoiner GUI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Zoom Autojoiner GUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Zoom Autojoiner GUI.  If not, see <https://www.gnu.org/licenses/>.

from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    REAL,
    DateTime
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from zoom_autojoiner_gui.constants import DB_URL


engine = create_engine(DB_URL)
# Session = sessionmaker(bind=engine)
Base = declarative_base()

class Meetings(Base):
    """Meetings 
    
    Class containing the Meetings table.
    """
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True)
    mtg_provider = Column(String)
    mtg_id = Column(String)
    mtg_password = Column(String)
    mtg_time = Column(DateTime)
    def __repr__(self):
        return "<Meeting(mtg_provider='%s', mtg_id='%s', mtg_password='%s')>" \
            % (self.mtg_provider, self.mtg_id, self.mtg_password)

Base.metadata.create_all(engine)


