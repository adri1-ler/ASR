import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Sports_Live_—_Football_·_Tennis_·_Rugby.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Sports_Live_—_Football_·_Tennis_·_Rugby API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "TennisSet", "description": "Operations for TennisSet entities"},
        {"name": "TennisSet Relationships", "description": "Manage TennisSet relationships"},
        {"name": "MatchPreview", "description": "Operations for MatchPreview entities"},
        {"name": "MatchPreview Relationships", "description": "Manage MatchPreview relationships"},
        {"name": "Team", "description": "Operations for Team entities"},
        {"name": "Team Relationships", "description": "Manage Team relationships"},
        {"name": "Standing", "description": "Operations for Standing entities"},
        {"name": "Standing Relationships", "description": "Manage Standing relationships"},
        {"name": "PreMatchOdds", "description": "Operations for PreMatchOdds entities"},
        {"name": "PreMatchOdds Relationships", "description": "Manage PreMatchOdds relationships"},
        {"name": "Sport", "description": "Operations for Sport entities"},
        {"name": "Sport Relationships", "description": "Manage Sport relationships"},
        {"name": "LineupPlayer", "description": "Operations for LineupPlayer entities"},
        {"name": "LineupPlayer Relationships", "description": "Manage LineupPlayer relationships"},
        {"name": "Reaction", "description": "Operations for Reaction entities"},
        {"name": "Reaction Relationships", "description": "Manage Reaction relationships"},
        {"name": "Lineup", "description": "Operations for Lineup entities"},
        {"name": "Lineup Relationships", "description": "Manage Lineup relationships"},
        {"name": "Player", "description": "Operations for Player entities"},
        {"name": "Player Relationships", "description": "Manage Player relationships"},
        {"name": "Stadium", "description": "Operations for Stadium entities"},
        {"name": "Stadium Relationships", "description": "Manage Stadium relationships"},
        {"name": "Notification", "description": "Operations for Notification entities"},
        {"name": "Notification Relationships", "description": "Manage Notification relationships"},
        {"name": "MediaFile", "description": "Operations for MediaFile entities"},
        {"name": "MediaFile Relationships", "description": "Manage MediaFile relationships"},
        {"name": "Message", "description": "Operations for Message entities"},
        {"name": "Message Relationships", "description": "Manage Message relationships"},
        {"name": "BracketSlot", "description": "Operations for BracketSlot entities"},
        {"name": "BracketSlot Relationships", "description": "Manage BracketSlot relationships"},
        {"name": "MatchEvent", "description": "Operations for MatchEvent entities"},
        {"name": "MatchEvent Relationships", "description": "Manage MatchEvent relationships"},
        {"name": "TournamentRound", "description": "Operations for TournamentRound entities"},
        {"name": "TournamentRound Relationships", "description": "Manage TournamentRound relationships"},
        {"name": "Match", "description": "Operations for Match entities"},
        {"name": "Match Relationships", "description": "Manage Match relationships"},
        {"name": "Friendship", "description": "Operations for Friendship entities"},
        {"name": "Friendship Relationships", "description": "Manage Friendship relationships"},
        {"name": "FavoritePlayer", "description": "Operations for FavoritePlayer entities"},
        {"name": "FavoritePlayer Relationships", "description": "Manage FavoritePlayer relationships"},
        {"name": "FavoriteTeam", "description": "Operations for FavoriteTeam entities"},
        {"name": "FavoriteTeam Relationships", "description": "Manage FavoriteTeam relationships"},
        {"name": "MatchStatistics", "description": "Operations for MatchStatistics entities"},
        {"name": "MatchStatistics Relationships", "description": "Manage MatchStatistics relationships"},
        {"name": "FavoriteCompetition", "description": "Operations for FavoriteCompetition entities"},
        {"name": "FavoriteCompetition Relationships", "description": "Manage FavoriteCompetition relationships"},
        {"name": "User", "description": "Operations for User entities"},
        {"name": "User Relationships", "description": "Manage User relationships"},
        {"name": "Competition", "description": "Operations for Competition entities"},
        {"name": "Competition Relationships", "description": "Manage Competition relationships"},
        {"name": "ChannelMember", "description": "Operations for ChannelMember entities"},
        {"name": "ChannelMember Relationships", "description": "Manage ChannelMember relationships"},
        {"name": "Channel", "description": "Operations for Channel entities"},
        {"name": "Channel Relationships", "description": "Manage Channel relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Sports_Live_—_Football_·_Tennis_·_Rugby API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["tennisset_count"] = database.query(TennisSet).count()
    stats["matchpreview_count"] = database.query(MatchPreview).count()
    stats["team_count"] = database.query(Team).count()
    stats["standing_count"] = database.query(Standing).count()
    stats["prematchodds_count"] = database.query(PreMatchOdds).count()
    stats["sport_count"] = database.query(Sport).count()
    stats["lineupplayer_count"] = database.query(LineupPlayer).count()
    stats["reaction_count"] = database.query(Reaction).count()
    stats["lineup_count"] = database.query(Lineup).count()
    stats["player_count"] = database.query(Player).count()
    stats["stadium_count"] = database.query(Stadium).count()
    stats["notification_count"] = database.query(Notification).count()
    stats["mediafile_count"] = database.query(MediaFile).count()
    stats["message_count"] = database.query(Message).count()
    stats["bracketslot_count"] = database.query(BracketSlot).count()
    stats["matchevent_count"] = database.query(MatchEvent).count()
    stats["tournamentround_count"] = database.query(TournamentRound).count()
    stats["match_count"] = database.query(Match).count()
    stats["friendship_count"] = database.query(Friendship).count()
    stats["favoriteplayer_count"] = database.query(FavoritePlayer).count()
    stats["favoriteteam_count"] = database.query(FavoriteTeam).count()
    stats["matchstatistics_count"] = database.query(MatchStatistics).count()
    stats["favoritecompetition_count"] = database.query(FavoriteCompetition).count()
    stats["user_count"] = database.query(User).count()
    stats["competition_count"] = database.query(Competition).count()
    stats["channelmember_count"] = database.query(ChannelMember).count()
    stats["channel_count"] = database.query(Channel).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   TennisSet functions
#
############################################

@app.get("/tennisset/", response_model=None, tags=["TennisSet"])
def get_all_tennisset(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(TennisSet)
        query = query.options(joinedload(TennisSet.match))
        tennisset_list = query.all()

        # Serialize with relationships included
        result = []
        for tennisset_item in tennisset_list:
            item_dict = tennisset_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if tennisset_item.match:
                related_obj = tennisset_item.match
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['match'] = related_dict
            else:
                item_dict['match'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(TennisSet).all()


@app.get("/tennisset/count/", response_model=None, tags=["TennisSet"])
def get_count_tennisset(database: Session = Depends(get_db)) -> dict:
    """Get the total count of TennisSet entities"""
    count = database.query(TennisSet).count()
    return {"count": count}


@app.get("/tennisset/paginated/", response_model=None, tags=["TennisSet"])
def get_paginated_tennisset(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of TennisSet entities"""
    total = database.query(TennisSet).count()
    tennisset_list = database.query(TennisSet).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": tennisset_list
    }


@app.get("/tennisset/search/", response_model=None, tags=["TennisSet"])
def search_tennisset(
    database: Session = Depends(get_db)
) -> list:
    """Search TennisSet entities by attributes"""
    query = database.query(TennisSet)


    results = query.all()
    return results


@app.get("/tennisset/{tennisset_id}/", response_model=None, tags=["TennisSet"])
async def get_tennisset(tennisset_id: int, database: Session = Depends(get_db)) -> TennisSet:
    db_tennisset = database.query(TennisSet).filter(TennisSet.id == tennisset_id).first()
    if db_tennisset is None:
        raise HTTPException(status_code=404, detail="TennisSet not found")

    response_data = {
        "tennisset": db_tennisset,
}
    return response_data



@app.post("/tennisset/", response_model=None, tags=["TennisSet"])
async def create_tennisset(tennisset_data: TennisSetCreate, database: Session = Depends(get_db)) -> TennisSet:

    if tennisset_data.match is not None:
        db_match = database.query(Match).filter(Match.id == tennisset_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
    else:
        raise HTTPException(status_code=400, detail="Match ID is required")

    db_tennisset = TennisSet(
        id=tennisset_data.id,        jeux_j2=tennisset_data.jeux_j2,        gagnant_id=tennisset_data.gagnant_id,        numero_set=tennisset_data.numero_set,        tb_points_j1=tennisset_data.tb_points_j1,        est_termine=tennisset_data.est_termine,        jeux_j1=tennisset_data.jeux_j1,        tb_points_j2=tennisset_data.tb_points_j2,        match_id=tennisset_data.match        )

    database.add(db_tennisset)
    database.commit()
    database.refresh(db_tennisset)




    return db_tennisset


@app.post("/tennisset/bulk/", response_model=None, tags=["TennisSet"])
async def bulk_create_tennisset(items: list[TennisSetCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple TennisSet entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.match:
                raise ValueError("Match ID is required")

            db_tennisset = TennisSet(
                id=item_data.id,                jeux_j2=item_data.jeux_j2,                gagnant_id=item_data.gagnant_id,                numero_set=item_data.numero_set,                tb_points_j1=item_data.tb_points_j1,                est_termine=item_data.est_termine,                jeux_j1=item_data.jeux_j1,                tb_points_j2=item_data.tb_points_j2,                match_id=item_data.match            )
            database.add(db_tennisset)
            database.flush()  # Get ID without committing
            created_items.append(db_tennisset.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} TennisSet entities"
    }


@app.delete("/tennisset/bulk/", response_model=None, tags=["TennisSet"])
async def bulk_delete_tennisset(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple TennisSet entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_tennisset = database.query(TennisSet).filter(TennisSet.id == item_id).first()
        if db_tennisset:
            database.delete(db_tennisset)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} TennisSet entities"
    }

@app.put("/tennisset/{tennisset_id}/", response_model=None, tags=["TennisSet"])
async def update_tennisset(tennisset_id: int, tennisset_data: TennisSetCreate, database: Session = Depends(get_db)) -> TennisSet:
    db_tennisset = database.query(TennisSet).filter(TennisSet.id == tennisset_id).first()
    if db_tennisset is None:
        raise HTTPException(status_code=404, detail="TennisSet not found")

    setattr(db_tennisset, 'id', tennisset_data.id)
    setattr(db_tennisset, 'jeux_j2', tennisset_data.jeux_j2)
    setattr(db_tennisset, 'gagnant_id', tennisset_data.gagnant_id)
    setattr(db_tennisset, 'numero_set', tennisset_data.numero_set)
    setattr(db_tennisset, 'tb_points_j1', tennisset_data.tb_points_j1)
    setattr(db_tennisset, 'est_termine', tennisset_data.est_termine)
    setattr(db_tennisset, 'jeux_j1', tennisset_data.jeux_j1)
    setattr(db_tennisset, 'tb_points_j2', tennisset_data.tb_points_j2)
    if tennisset_data.match is not None:
        db_match = database.query(Match).filter(Match.id == tennisset_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
        setattr(db_tennisset, 'match_id', tennisset_data.match)
    database.commit()
    database.refresh(db_tennisset)

    return db_tennisset


@app.delete("/tennisset/{tennisset_id}/", response_model=None, tags=["TennisSet"])
async def delete_tennisset(tennisset_id: int, database: Session = Depends(get_db)):
    db_tennisset = database.query(TennisSet).filter(TennisSet.id == tennisset_id).first()
    if db_tennisset is None:
        raise HTTPException(status_code=404, detail="TennisSet not found")
    database.delete(db_tennisset)
    database.commit()
    return db_tennisset






############################################
#
#   MatchPreview functions
#
############################################

@app.get("/matchpreview/", response_model=None, tags=["MatchPreview"])
def get_all_matchpreview(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(MatchPreview)
        query = query.options(joinedload(MatchPreview.match))
        matchpreview_list = query.all()

        # Serialize with relationships included
        result = []
        for matchpreview_item in matchpreview_list:
            item_dict = matchpreview_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if matchpreview_item.match:
                related_obj = matchpreview_item.match
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['match'] = related_dict
            else:
                item_dict['match'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(MatchPreview).all()


@app.get("/matchpreview/count/", response_model=None, tags=["MatchPreview"])
def get_count_matchpreview(database: Session = Depends(get_db)) -> dict:
    """Get the total count of MatchPreview entities"""
    count = database.query(MatchPreview).count()
    return {"count": count}


@app.get("/matchpreview/paginated/", response_model=None, tags=["MatchPreview"])
def get_paginated_matchpreview(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of MatchPreview entities"""
    total = database.query(MatchPreview).count()
    matchpreview_list = database.query(MatchPreview).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": matchpreview_list
    }


@app.get("/matchpreview/search/", response_model=None, tags=["MatchPreview"])
def search_matchpreview(
    database: Session = Depends(get_db)
) -> list:
    """Search MatchPreview entities by attributes"""
    query = database.query(MatchPreview)


    results = query.all()
    return results


@app.get("/matchpreview/{matchpreview_id}/", response_model=None, tags=["MatchPreview"])
async def get_matchpreview(matchpreview_id: int, database: Session = Depends(get_db)) -> MatchPreview:
    db_matchpreview = database.query(MatchPreview).filter(MatchPreview.id == matchpreview_id).first()
    if db_matchpreview is None:
        raise HTTPException(status_code=404, detail="MatchPreview not found")

    response_data = {
        "matchpreview": db_matchpreview,
}
    return response_data



@app.post("/matchpreview/", response_model=None, tags=["MatchPreview"])
async def create_matchpreview(matchpreview_data: MatchPreviewCreate, database: Session = Depends(get_db)) -> MatchPreview:

    if matchpreview_data.match is not None:
        db_match = database.query(Match).filter(Match.id == matchpreview_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
    else:
        raise HTTPException(status_code=400, detail="Match ID is required")

    db_matchpreview = MatchPreview(
        forme_exterieur=matchpreview_data.forme_exterieur,        h2h_victoires_ext=matchpreview_data.h2h_victoires_ext,        id=matchpreview_data.id,        enjeu=matchpreview_data.enjeu,        h2h_victoires_dom=matchpreview_data.h2h_victoires_dom,        absents_domicile=matchpreview_data.absents_domicile,        forme_domicile=matchpreview_data.forme_domicile,        publie_le=matchpreview_data.publie_le,        h2h_nuls=matchpreview_data.h2h_nuls,        absents_exterieur=matchpreview_data.absents_exterieur,        match_id=matchpreview_data.match        )

    database.add(db_matchpreview)
    database.commit()
    database.refresh(db_matchpreview)




    return db_matchpreview


@app.post("/matchpreview/bulk/", response_model=None, tags=["MatchPreview"])
async def bulk_create_matchpreview(items: list[MatchPreviewCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple MatchPreview entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.match:
                raise ValueError("Match ID is required")

            db_matchpreview = MatchPreview(
                forme_exterieur=item_data.forme_exterieur,                h2h_victoires_ext=item_data.h2h_victoires_ext,                id=item_data.id,                enjeu=item_data.enjeu,                h2h_victoires_dom=item_data.h2h_victoires_dom,                absents_domicile=item_data.absents_domicile,                forme_domicile=item_data.forme_domicile,                publie_le=item_data.publie_le,                h2h_nuls=item_data.h2h_nuls,                absents_exterieur=item_data.absents_exterieur,                match_id=item_data.match            )
            database.add(db_matchpreview)
            database.flush()  # Get ID without committing
            created_items.append(db_matchpreview.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} MatchPreview entities"
    }


@app.delete("/matchpreview/bulk/", response_model=None, tags=["MatchPreview"])
async def bulk_delete_matchpreview(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple MatchPreview entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_matchpreview = database.query(MatchPreview).filter(MatchPreview.id == item_id).first()
        if db_matchpreview:
            database.delete(db_matchpreview)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} MatchPreview entities"
    }

@app.put("/matchpreview/{matchpreview_id}/", response_model=None, tags=["MatchPreview"])
async def update_matchpreview(matchpreview_id: int, matchpreview_data: MatchPreviewCreate, database: Session = Depends(get_db)) -> MatchPreview:
    db_matchpreview = database.query(MatchPreview).filter(MatchPreview.id == matchpreview_id).first()
    if db_matchpreview is None:
        raise HTTPException(status_code=404, detail="MatchPreview not found")

    setattr(db_matchpreview, 'forme_exterieur', matchpreview_data.forme_exterieur)
    setattr(db_matchpreview, 'h2h_victoires_ext', matchpreview_data.h2h_victoires_ext)
    setattr(db_matchpreview, 'id', matchpreview_data.id)
    setattr(db_matchpreview, 'enjeu', matchpreview_data.enjeu)
    setattr(db_matchpreview, 'h2h_victoires_dom', matchpreview_data.h2h_victoires_dom)
    setattr(db_matchpreview, 'absents_domicile', matchpreview_data.absents_domicile)
    setattr(db_matchpreview, 'forme_domicile', matchpreview_data.forme_domicile)
    setattr(db_matchpreview, 'publie_le', matchpreview_data.publie_le)
    setattr(db_matchpreview, 'h2h_nuls', matchpreview_data.h2h_nuls)
    setattr(db_matchpreview, 'absents_exterieur', matchpreview_data.absents_exterieur)
    if matchpreview_data.match is not None:
        db_match = database.query(Match).filter(Match.id == matchpreview_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
        setattr(db_matchpreview, 'match_id', matchpreview_data.match)
    database.commit()
    database.refresh(db_matchpreview)

    return db_matchpreview


@app.delete("/matchpreview/{matchpreview_id}/", response_model=None, tags=["MatchPreview"])
async def delete_matchpreview(matchpreview_id: int, database: Session = Depends(get_db)):
    db_matchpreview = database.query(MatchPreview).filter(MatchPreview.id == matchpreview_id).first()
    if db_matchpreview is None:
        raise HTTPException(status_code=404, detail="MatchPreview not found")
    database.delete(db_matchpreview)
    database.commit()
    return db_matchpreview






############################################
#
#   Team functions
#
############################################

@app.get("/team/", response_model=None, tags=["Team"])
def get_all_team(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Team)
        query = query.options(joinedload(Team.stade_domicile))
        team_list = query.all()

        # Serialize with relationships included
        result = []
        for team_item in team_list:
            item_dict = team_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if team_item.stade_domicile:
                related_obj = team_item.stade_domicile
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['stade_domicile'] = related_dict
            else:
                item_dict['stade_domicile'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            competition_list = database.query(Competition).join(competition_team, Competition.id == competition_team.c.competitions).filter(competition_team.c.equipes == team_item.id).all()
            item_dict['competitions'] = []
            for competition_obj in competition_list:
                competition_dict = competition_obj.__dict__.copy()
                competition_dict.pop('_sa_instance_state', None)
                item_dict['competitions'].append(competition_dict)
            matchevent_list = database.query(MatchEvent).filter(MatchEvent.equipe_id == team_item.id).all()
            item_dict['evenements_equipe'] = []
            for matchevent_obj in matchevent_list:
                matchevent_dict = matchevent_obj.__dict__.copy()
                matchevent_dict.pop('_sa_instance_state', None)
                item_dict['evenements_equipe'].append(matchevent_dict)
            player_list = database.query(Player).filter(Player.equipe_id == team_item.id).all()
            item_dict['joueurs'] = []
            for player_obj in player_list:
                player_dict = player_obj.__dict__.copy()
                player_dict.pop('_sa_instance_state', None)
                item_dict['joueurs'].append(player_dict)
            standing_list = database.query(Standing).filter(Standing.equipe_id == team_item.id).all()
            item_dict['classements'] = []
            for standing_obj in standing_list:
                standing_dict = standing_obj.__dict__.copy()
                standing_dict.pop('_sa_instance_state', None)
                item_dict['classements'].append(standing_dict)
            lineup_list = database.query(Lineup).filter(Lineup.equipe_id == team_item.id).all()
            item_dict['lineups'] = []
            for lineup_obj in lineup_list:
                lineup_dict = lineup_obj.__dict__.copy()
                lineup_dict.pop('_sa_instance_state', None)
                item_dict['lineups'].append(lineup_dict)
            match_list = database.query(Match).filter(Match.equipe_domicile_id == team_item.id).all()
            item_dict['matchs_a_domicile'] = []
            for match_obj in match_list:
                match_dict = match_obj.__dict__.copy()
                match_dict.pop('_sa_instance_state', None)
                item_dict['matchs_a_domicile'].append(match_dict)
            match_list = database.query(Match).filter(Match.equipe_exterieure_id == team_item.id).all()
            item_dict['matchs_a_exterieur'] = []
            for match_obj in match_list:
                match_dict = match_obj.__dict__.copy()
                match_dict.pop('_sa_instance_state', None)
                item_dict['matchs_a_exterieur'].append(match_dict)
            favoriteteam_list = database.query(FavoriteTeam).filter(FavoriteTeam.equipe_id == team_item.id).all()
            item_dict['fans'] = []
            for favoriteteam_obj in favoriteteam_list:
                favoriteteam_dict = favoriteteam_obj.__dict__.copy()
                favoriteteam_dict.pop('_sa_instance_state', None)
                item_dict['fans'].append(favoriteteam_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Team).all()


@app.get("/team/count/", response_model=None, tags=["Team"])
def get_count_team(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Team entities"""
    count = database.query(Team).count()
    return {"count": count}


@app.get("/team/paginated/", response_model=None, tags=["Team"])
def get_paginated_team(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Team entities"""
    total = database.query(Team).count()
    team_list = database.query(Team).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": team_list
        }

    result = []
    for team_item in team_list:
        competition_ids = database.query(competition_team.c.competitions).filter(competition_team.c.equipes == team_item.id).all()
        evenements_equipe_ids = database.query(MatchEvent.id).filter(MatchEvent.equipe_id == team_item.id).all()
        joueurs_ids = database.query(Player.id).filter(Player.equipe_id == team_item.id).all()
        classements_ids = database.query(Standing.id).filter(Standing.equipe_id == team_item.id).all()
        lineups_ids = database.query(Lineup.id).filter(Lineup.equipe_id == team_item.id).all()
        matchs_a_domicile_ids = database.query(Match.id).filter(Match.equipe_domicile_id == team_item.id).all()
        matchs_a_exterieur_ids = database.query(Match.id).filter(Match.equipe_exterieure_id == team_item.id).all()
        fans_ids = database.query(FavoriteTeam.id).filter(FavoriteTeam.equipe_id == team_item.id).all()
        item_data = {
            "team": team_item,
            "competition_ids": [x[0] for x in competition_ids],
            "evenements_equipe_ids": [x[0] for x in evenements_equipe_ids],            "joueurs_ids": [x[0] for x in joueurs_ids],            "classements_ids": [x[0] for x in classements_ids],            "lineups_ids": [x[0] for x in lineups_ids],            "matchs_a_domicile_ids": [x[0] for x in matchs_a_domicile_ids],            "matchs_a_exterieur_ids": [x[0] for x in matchs_a_exterieur_ids],            "fans_ids": [x[0] for x in fans_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/team/search/", response_model=None, tags=["Team"])
def search_team(
    database: Session = Depends(get_db)
) -> list:
    """Search Team entities by attributes"""
    query = database.query(Team)


    results = query.all()
    return results


@app.get("/team/{team_id}/", response_model=None, tags=["Team"])
async def get_team(team_id: int, database: Session = Depends(get_db)) -> Team:
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    competition_ids = database.query(competition_team.c.competitions).filter(competition_team.c.equipes == db_team.id).all()
    evenements_equipe_ids = database.query(MatchEvent.id).filter(MatchEvent.equipe_id == db_team.id).all()
    joueurs_ids = database.query(Player.id).filter(Player.equipe_id == db_team.id).all()
    classements_ids = database.query(Standing.id).filter(Standing.equipe_id == db_team.id).all()
    lineups_ids = database.query(Lineup.id).filter(Lineup.equipe_id == db_team.id).all()
    matchs_a_domicile_ids = database.query(Match.id).filter(Match.equipe_domicile_id == db_team.id).all()
    matchs_a_exterieur_ids = database.query(Match.id).filter(Match.equipe_exterieure_id == db_team.id).all()
    fans_ids = database.query(FavoriteTeam.id).filter(FavoriteTeam.equipe_id == db_team.id).all()
    response_data = {
        "team": db_team,
        "competition_ids": [x[0] for x in competition_ids],
        "evenements_equipe_ids": [x[0] for x in evenements_equipe_ids],        "joueurs_ids": [x[0] for x in joueurs_ids],        "classements_ids": [x[0] for x in classements_ids],        "lineups_ids": [x[0] for x in lineups_ids],        "matchs_a_domicile_ids": [x[0] for x in matchs_a_domicile_ids],        "matchs_a_exterieur_ids": [x[0] for x in matchs_a_exterieur_ids],        "fans_ids": [x[0] for x in fans_ids]}
    return response_data



@app.post("/team/", response_model=None, tags=["Team"])
async def create_team(team_data: TeamCreate, database: Session = Depends(get_db)) -> Team:

    if team_data.stade_domicile :
        db_stade_domicile = database.query(Stadium).filter(Stadium.id == team_data.stade_domicile).first()
        if not db_stade_domicile:
            raise HTTPException(status_code=400, detail="Stadium not found")
    if team_data.competitions:
        for id in team_data.competitions:
            # Entity already validated before creation
            db_competition = database.query(Competition).filter(Competition.id == id).first()
            if not db_competition:
                raise HTTPException(status_code=404, detail=f"Competition with ID {id} not found")

    db_team = Team(
        abreviation=team_data.abreviation,        nom=team_data.nom,        ville=team_data.ville,        id=team_data.id,        pays=team_data.pays,        logo_url=team_data.logo_url,        stade=team_data.stade,        stade_domicile_id=team_data.stade_domicile        )

    database.add(db_team)
    database.commit()
    database.refresh(db_team)

    if team_data.evenements_equipe:
        # Validate that all MatchEvent IDs exist
        for matchevent_id in team_data.evenements_equipe:
            db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
            if not db_matchevent:
                raise HTTPException(status_code=400, detail=f"MatchEvent with id {matchevent_id} not found")

        # Update the related entities with the new foreign key
        database.query(MatchEvent).filter(MatchEvent.id.in_(team_data.evenements_equipe)).update(
            {MatchEvent.equipe_id: db_team.id}, synchronize_session=False
        )
        database.commit()
    if team_data.joueurs:
        # Validate that all Player IDs exist
        for player_id in team_data.joueurs:
            db_player = database.query(Player).filter(Player.id == player_id).first()
            if not db_player:
                raise HTTPException(status_code=400, detail=f"Player with id {player_id} not found")

        # Update the related entities with the new foreign key
        database.query(Player).filter(Player.id.in_(team_data.joueurs)).update(
            {Player.equipe_id: db_team.id}, synchronize_session=False
        )
        database.commit()
    if team_data.classements:
        # Validate that all Standing IDs exist
        for standing_id in team_data.classements:
            db_standing = database.query(Standing).filter(Standing.id == standing_id).first()
            if not db_standing:
                raise HTTPException(status_code=400, detail=f"Standing with id {standing_id} not found")

        # Update the related entities with the new foreign key
        database.query(Standing).filter(Standing.id.in_(team_data.classements)).update(
            {Standing.equipe_id: db_team.id}, synchronize_session=False
        )
        database.commit()
    if team_data.lineups:
        # Validate that all Lineup IDs exist
        for lineup_id in team_data.lineups:
            db_lineup = database.query(Lineup).filter(Lineup.id == lineup_id).first()
            if not db_lineup:
                raise HTTPException(status_code=400, detail=f"Lineup with id {lineup_id} not found")

        # Update the related entities with the new foreign key
        database.query(Lineup).filter(Lineup.id.in_(team_data.lineups)).update(
            {Lineup.equipe_id: db_team.id}, synchronize_session=False
        )
        database.commit()
    if team_data.matchs_a_domicile:
        # Validate that all Match IDs exist
        for match_id in team_data.matchs_a_domicile:
            db_match = database.query(Match).filter(Match.id == match_id).first()
            if not db_match:
                raise HTTPException(status_code=400, detail=f"Match with id {match_id} not found")

        # Update the related entities with the new foreign key
        database.query(Match).filter(Match.id.in_(team_data.matchs_a_domicile)).update(
            {Match.equipe_domicile_id: db_team.id}, synchronize_session=False
        )
        database.commit()
    if team_data.matchs_a_exterieur:
        # Validate that all Match IDs exist
        for match_id in team_data.matchs_a_exterieur:
            db_match = database.query(Match).filter(Match.id == match_id).first()
            if not db_match:
                raise HTTPException(status_code=400, detail=f"Match with id {match_id} not found")

        # Update the related entities with the new foreign key
        database.query(Match).filter(Match.id.in_(team_data.matchs_a_exterieur)).update(
            {Match.equipe_exterieure_id: db_team.id}, synchronize_session=False
        )
        database.commit()
    if team_data.fans:
        # Validate that all FavoriteTeam IDs exist
        for favoriteteam_id in team_data.fans:
            db_favoriteteam = database.query(FavoriteTeam).filter(FavoriteTeam.id == favoriteteam_id).first()
            if not db_favoriteteam:
                raise HTTPException(status_code=400, detail=f"FavoriteTeam with id {favoriteteam_id} not found")

        # Update the related entities with the new foreign key
        database.query(FavoriteTeam).filter(FavoriteTeam.id.in_(team_data.fans)).update(
            {FavoriteTeam.equipe_id: db_team.id}, synchronize_session=False
        )
        database.commit()

    if team_data.competitions:
        for id in team_data.competitions:
            # Entity already validated before creation
            db_competition = database.query(Competition).filter(Competition.id == id).first()
            # Create the association
            association = competition_team.insert().values(equipes=db_team.id, competitions=db_competition.id)
            database.execute(association)
            database.commit()


    competition_ids = database.query(competition_team.c.competitions).filter(competition_team.c.equipes == db_team.id).all()
    evenements_equipe_ids = database.query(MatchEvent.id).filter(MatchEvent.equipe_id == db_team.id).all()
    joueurs_ids = database.query(Player.id).filter(Player.equipe_id == db_team.id).all()
    classements_ids = database.query(Standing.id).filter(Standing.equipe_id == db_team.id).all()
    lineups_ids = database.query(Lineup.id).filter(Lineup.equipe_id == db_team.id).all()
    matchs_a_domicile_ids = database.query(Match.id).filter(Match.equipe_domicile_id == db_team.id).all()
    matchs_a_exterieur_ids = database.query(Match.id).filter(Match.equipe_exterieure_id == db_team.id).all()
    fans_ids = database.query(FavoriteTeam.id).filter(FavoriteTeam.equipe_id == db_team.id).all()
    response_data = {
        "team": db_team,
        "competition_ids": [x[0] for x in competition_ids],
        "evenements_equipe_ids": [x[0] for x in evenements_equipe_ids],        "joueurs_ids": [x[0] for x in joueurs_ids],        "classements_ids": [x[0] for x in classements_ids],        "lineups_ids": [x[0] for x in lineups_ids],        "matchs_a_domicile_ids": [x[0] for x in matchs_a_domicile_ids],        "matchs_a_exterieur_ids": [x[0] for x in matchs_a_exterieur_ids],        "fans_ids": [x[0] for x in fans_ids]    }
    return response_data


@app.post("/team/bulk/", response_model=None, tags=["Team"])
async def bulk_create_team(items: list[TeamCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Team entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_team = Team(
                abreviation=item_data.abreviation,                nom=item_data.nom,                ville=item_data.ville,                id=item_data.id,                pays=item_data.pays,                logo_url=item_data.logo_url,                stade=item_data.stade,                stade_domicile_id=item_data.stade_domicile            )
            database.add(db_team)
            database.flush()  # Get ID without committing
            created_items.append(db_team.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Team entities"
    }


@app.delete("/team/bulk/", response_model=None, tags=["Team"])
async def bulk_delete_team(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Team entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_team = database.query(Team).filter(Team.id == item_id).first()
        if db_team:
            database.delete(db_team)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Team entities"
    }

@app.put("/team/{team_id}/", response_model=None, tags=["Team"])
async def update_team(team_id: int, team_data: TeamCreate, database: Session = Depends(get_db)) -> Team:
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    setattr(db_team, 'abreviation', team_data.abreviation)
    setattr(db_team, 'nom', team_data.nom)
    setattr(db_team, 'ville', team_data.ville)
    setattr(db_team, 'id', team_data.id)
    setattr(db_team, 'pays', team_data.pays)
    setattr(db_team, 'logo_url', team_data.logo_url)
    setattr(db_team, 'stade', team_data.stade)
    if team_data.stade_domicile is not None:
        db_stade_domicile = database.query(Stadium).filter(Stadium.id == team_data.stade_domicile).first()
        if not db_stade_domicile:
            raise HTTPException(status_code=400, detail="Stadium not found")
        setattr(db_team, 'stade_domicile_id', team_data.stade_domicile)
    else:
        setattr(db_team, 'stade_domicile_id', None)
    if team_data.evenements_equipe is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(MatchEvent).filter(MatchEvent.equipe_id == db_team.id).update(
            {MatchEvent.equipe_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if team_data.evenements_equipe:
            # Validate that all IDs exist
            for matchevent_id in team_data.evenements_equipe:
                db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
                if not db_matchevent:
                    raise HTTPException(status_code=400, detail=f"MatchEvent with id {matchevent_id} not found")

            # Update the related entities with the new foreign key
            database.query(MatchEvent).filter(MatchEvent.id.in_(team_data.evenements_equipe)).update(
                {MatchEvent.equipe_id: db_team.id}, synchronize_session=False
            )
    if team_data.joueurs is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Player).filter(Player.equipe_id == db_team.id).update(
            {Player.equipe_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if team_data.joueurs:
            # Validate that all IDs exist
            for player_id in team_data.joueurs:
                db_player = database.query(Player).filter(Player.id == player_id).first()
                if not db_player:
                    raise HTTPException(status_code=400, detail=f"Player with id {player_id} not found")

            # Update the related entities with the new foreign key
            database.query(Player).filter(Player.id.in_(team_data.joueurs)).update(
                {Player.equipe_id: db_team.id}, synchronize_session=False
            )
    if team_data.classements is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Standing).filter(Standing.equipe_id == db_team.id).update(
            {Standing.equipe_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if team_data.classements:
            # Validate that all IDs exist
            for standing_id in team_data.classements:
                db_standing = database.query(Standing).filter(Standing.id == standing_id).first()
                if not db_standing:
                    raise HTTPException(status_code=400, detail=f"Standing with id {standing_id} not found")

            # Update the related entities with the new foreign key
            database.query(Standing).filter(Standing.id.in_(team_data.classements)).update(
                {Standing.equipe_id: db_team.id}, synchronize_session=False
            )
    if team_data.lineups is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Lineup).filter(Lineup.equipe_id == db_team.id).update(
            {Lineup.equipe_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if team_data.lineups:
            # Validate that all IDs exist
            for lineup_id in team_data.lineups:
                db_lineup = database.query(Lineup).filter(Lineup.id == lineup_id).first()
                if not db_lineup:
                    raise HTTPException(status_code=400, detail=f"Lineup with id {lineup_id} not found")

            # Update the related entities with the new foreign key
            database.query(Lineup).filter(Lineup.id.in_(team_data.lineups)).update(
                {Lineup.equipe_id: db_team.id}, synchronize_session=False
            )
    if team_data.matchs_a_domicile is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Match).filter(Match.equipe_domicile_id == db_team.id).update(
            {Match.equipe_domicile_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if team_data.matchs_a_domicile:
            # Validate that all IDs exist
            for match_id in team_data.matchs_a_domicile:
                db_match = database.query(Match).filter(Match.id == match_id).first()
                if not db_match:
                    raise HTTPException(status_code=400, detail=f"Match with id {match_id} not found")

            # Update the related entities with the new foreign key
            database.query(Match).filter(Match.id.in_(team_data.matchs_a_domicile)).update(
                {Match.equipe_domicile_id: db_team.id}, synchronize_session=False
            )
    if team_data.matchs_a_exterieur is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Match).filter(Match.equipe_exterieure_id == db_team.id).update(
            {Match.equipe_exterieure_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if team_data.matchs_a_exterieur:
            # Validate that all IDs exist
            for match_id in team_data.matchs_a_exterieur:
                db_match = database.query(Match).filter(Match.id == match_id).first()
                if not db_match:
                    raise HTTPException(status_code=400, detail=f"Match with id {match_id} not found")

            # Update the related entities with the new foreign key
            database.query(Match).filter(Match.id.in_(team_data.matchs_a_exterieur)).update(
                {Match.equipe_exterieure_id: db_team.id}, synchronize_session=False
            )
    if team_data.fans is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(FavoriteTeam).filter(FavoriteTeam.equipe_id == db_team.id).update(
            {FavoriteTeam.equipe_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if team_data.fans:
            # Validate that all IDs exist
            for favoriteteam_id in team_data.fans:
                db_favoriteteam = database.query(FavoriteTeam).filter(FavoriteTeam.id == favoriteteam_id).first()
                if not db_favoriteteam:
                    raise HTTPException(status_code=400, detail=f"FavoriteTeam with id {favoriteteam_id} not found")

            # Update the related entities with the new foreign key
            database.query(FavoriteTeam).filter(FavoriteTeam.id.in_(team_data.fans)).update(
                {FavoriteTeam.equipe_id: db_team.id}, synchronize_session=False
            )
    existing_competition_ids = [assoc.competitions for assoc in database.execute(
        competition_team.select().where(competition_team.c.equipes == db_team.id))]

    competitions_to_remove = set(existing_competition_ids) - set(team_data.competitions)
    for competition_id in competitions_to_remove:
        association = competition_team.delete().where(
            (competition_team.c.equipes == db_team.id) & (competition_team.c.competitions == competition_id))
        database.execute(association)

    new_competition_ids = set(team_data.competitions) - set(existing_competition_ids)
    for competition_id in new_competition_ids:
        db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
        if db_competition is None:
            raise HTTPException(status_code=404, detail=f"Competition with ID {competition_id} not found")
        association = competition_team.insert().values(competitions=db_competition.id, equipes=db_team.id)
        database.execute(association)
    database.commit()
    database.refresh(db_team)

    competition_ids = database.query(competition_team.c.competitions).filter(competition_team.c.equipes == db_team.id).all()
    evenements_equipe_ids = database.query(MatchEvent.id).filter(MatchEvent.equipe_id == db_team.id).all()
    joueurs_ids = database.query(Player.id).filter(Player.equipe_id == db_team.id).all()
    classements_ids = database.query(Standing.id).filter(Standing.equipe_id == db_team.id).all()
    lineups_ids = database.query(Lineup.id).filter(Lineup.equipe_id == db_team.id).all()
    matchs_a_domicile_ids = database.query(Match.id).filter(Match.equipe_domicile_id == db_team.id).all()
    matchs_a_exterieur_ids = database.query(Match.id).filter(Match.equipe_exterieure_id == db_team.id).all()
    fans_ids = database.query(FavoriteTeam.id).filter(FavoriteTeam.equipe_id == db_team.id).all()
    response_data = {
        "team": db_team,
        "competition_ids": [x[0] for x in competition_ids],
        "evenements_equipe_ids": [x[0] for x in evenements_equipe_ids],        "joueurs_ids": [x[0] for x in joueurs_ids],        "classements_ids": [x[0] for x in classements_ids],        "lineups_ids": [x[0] for x in lineups_ids],        "matchs_a_domicile_ids": [x[0] for x in matchs_a_domicile_ids],        "matchs_a_exterieur_ids": [x[0] for x in matchs_a_exterieur_ids],        "fans_ids": [x[0] for x in fans_ids]    }
    return response_data


@app.delete("/team/{team_id}/", response_model=None, tags=["Team"])
async def delete_team(team_id: int, database: Session = Depends(get_db)):
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    database.delete(db_team)
    database.commit()
    return db_team

@app.post("/team/{team_id}/competitions/{competition_id}/", response_model=None, tags=["Team Relationships"])
async def add_competitions_to_team(team_id: int, competition_id: int, database: Session = Depends(get_db)):
    """Add a Competition to this Team's competitions relationship"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    # Check if relationship already exists
    existing = database.query(competition_team).filter(
        (competition_team.c.equipes == team_id) &
        (competition_team.c.competitions == competition_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = competition_team.insert().values(equipes=team_id, competitions=competition_id)
    database.execute(association)
    database.commit()

    return {"message": "Competition added to competitions successfully"}


@app.delete("/team/{team_id}/competitions/{competition_id}/", response_model=None, tags=["Team Relationships"])
async def remove_competitions_from_team(team_id: int, competition_id: int, database: Session = Depends(get_db)):
    """Remove a Competition from this Team's competitions relationship"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    # Check if relationship exists
    existing = database.query(competition_team).filter(
        (competition_team.c.equipes == team_id) &
        (competition_team.c.competitions == competition_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = competition_team.delete().where(
        (competition_team.c.equipes == team_id) &
        (competition_team.c.competitions == competition_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Competition removed from competitions successfully"}


@app.get("/team/{team_id}/competitions/", response_model=None, tags=["Team Relationships"])
async def get_competitions_of_team(team_id: int, database: Session = Depends(get_db)):
    """Get all Competition entities related to this Team through competitions"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    competition_ids = database.query(competition_team.c.competitions).filter(competition_team.c.equipes == team_id).all()
    competition_list = database.query(Competition).filter(Competition.id.in_([id[0] for id in competition_ids])).all()

    return {
        "team_id": team_id,
        "competitions_count": len(competition_list),
        "competitions": competition_list
    }


@app.get("/team/{team_id}/evenements_equipe/", response_model=None, tags=["Team Relationships"])
async def get_evenements_equipe_of_team(team_id: int, database: Session = Depends(get_db)):
    """Get all MatchEvent entities related to this Team through evenements_equipe"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    evenements_equipe_list = database.query(MatchEvent).filter(MatchEvent.equipe_id == team_id).all()

    return {
        "team_id": team_id,
        "evenements_equipe_count": len(evenements_equipe_list),
        "evenements_equipe": evenements_equipe_list
    }

@app.get("/team/{team_id}/joueurs/", response_model=None, tags=["Team Relationships"])
async def get_joueurs_of_team(team_id: int, database: Session = Depends(get_db)):
    """Get all Player entities related to this Team through joueurs"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    joueurs_list = database.query(Player).filter(Player.equipe_id == team_id).all()

    return {
        "team_id": team_id,
        "joueurs_count": len(joueurs_list),
        "joueurs": joueurs_list
    }

@app.get("/team/{team_id}/classements/", response_model=None, tags=["Team Relationships"])
async def get_classements_of_team(team_id: int, database: Session = Depends(get_db)):
    """Get all Standing entities related to this Team through classements"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    classements_list = database.query(Standing).filter(Standing.equipe_id == team_id).all()

    return {
        "team_id": team_id,
        "classements_count": len(classements_list),
        "classements": classements_list
    }

@app.get("/team/{team_id}/lineups/", response_model=None, tags=["Team Relationships"])
async def get_lineups_of_team(team_id: int, database: Session = Depends(get_db)):
    """Get all Lineup entities related to this Team through lineups"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    lineups_list = database.query(Lineup).filter(Lineup.equipe_id == team_id).all()

    return {
        "team_id": team_id,
        "lineups_count": len(lineups_list),
        "lineups": lineups_list
    }

@app.get("/team/{team_id}/matchs_a_domicile/", response_model=None, tags=["Team Relationships"])
async def get_matchs_a_domicile_of_team(team_id: int, database: Session = Depends(get_db)):
    """Get all Match entities related to this Team through matchs_a_domicile"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    matchs_a_domicile_list = database.query(Match).filter(Match.equipe_domicile_id == team_id).all()

    return {
        "team_id": team_id,
        "matchs_a_domicile_count": len(matchs_a_domicile_list),
        "matchs_a_domicile": matchs_a_domicile_list
    }

@app.get("/team/{team_id}/matchs_a_exterieur/", response_model=None, tags=["Team Relationships"])
async def get_matchs_a_exterieur_of_team(team_id: int, database: Session = Depends(get_db)):
    """Get all Match entities related to this Team through matchs_a_exterieur"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    matchs_a_exterieur_list = database.query(Match).filter(Match.equipe_exterieure_id == team_id).all()

    return {
        "team_id": team_id,
        "matchs_a_exterieur_count": len(matchs_a_exterieur_list),
        "matchs_a_exterieur": matchs_a_exterieur_list
    }

@app.get("/team/{team_id}/fans/", response_model=None, tags=["Team Relationships"])
async def get_fans_of_team(team_id: int, database: Session = Depends(get_db)):
    """Get all FavoriteTeam entities related to this Team through fans"""
    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    fans_list = database.query(FavoriteTeam).filter(FavoriteTeam.equipe_id == team_id).all()

    return {
        "team_id": team_id,
        "fans_count": len(fans_list),
        "fans": fans_list
    }





############################################
#
#   Standing functions
#
############################################

@app.get("/standing/", response_model=None, tags=["Standing"])
def get_all_standing(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Standing)
        query = query.options(joinedload(Standing.competition))
        query = query.options(joinedload(Standing.equipe))
        standing_list = query.all()

        # Serialize with relationships included
        result = []
        for standing_item in standing_list:
            item_dict = standing_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if standing_item.competition:
                related_obj = standing_item.competition
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['competition'] = related_dict
            else:
                item_dict['competition'] = None
            if standing_item.equipe:
                related_obj = standing_item.equipe
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['equipe'] = related_dict
            else:
                item_dict['equipe'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Standing).all()


@app.get("/standing/count/", response_model=None, tags=["Standing"])
def get_count_standing(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Standing entities"""
    count = database.query(Standing).count()
    return {"count": count}


@app.get("/standing/paginated/", response_model=None, tags=["Standing"])
def get_paginated_standing(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Standing entities"""
    total = database.query(Standing).count()
    standing_list = database.query(Standing).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": standing_list
    }


@app.get("/standing/search/", response_model=None, tags=["Standing"])
def search_standing(
    database: Session = Depends(get_db)
) -> list:
    """Search Standing entities by attributes"""
    query = database.query(Standing)


    results = query.all()
    return results


@app.get("/standing/{standing_id}/", response_model=None, tags=["Standing"])
async def get_standing(standing_id: int, database: Session = Depends(get_db)) -> Standing:
    db_standing = database.query(Standing).filter(Standing.id == standing_id).first()
    if db_standing is None:
        raise HTTPException(status_code=404, detail="Standing not found")

    response_data = {
        "standing": db_standing,
}
    return response_data



@app.post("/standing/", response_model=None, tags=["Standing"])
async def create_standing(standing_data: StandingCreate, database: Session = Depends(get_db)) -> Standing:

    if standing_data.competition is not None:
        db_competition = database.query(Competition).filter(Competition.id == standing_data.competition).first()
        if not db_competition:
            raise HTTPException(status_code=400, detail="Competition not found")
    else:
        raise HTTPException(status_code=400, detail="Competition ID is required")
    if standing_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == standing_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
    else:
        raise HTTPException(status_code=400, detail="Team ID is required")

    db_standing = Standing(
        classement=standing_data.classement,        id=standing_data.id,        points_concedes=standing_data.points_concedes,        points=standing_data.points,        defaites=standing_data.defaites,        matchs_joues=standing_data.matchs_joues,        points_marques=standing_data.points_marques,        victoires=standing_data.victoires,        difference_points=standing_data.difference_points,        nuls=standing_data.nuls,        competition_id=standing_data.competition,        equipe_id=standing_data.equipe        )

    database.add(db_standing)
    database.commit()
    database.refresh(db_standing)




    return db_standing


@app.post("/standing/bulk/", response_model=None, tags=["Standing"])
async def bulk_create_standing(items: list[StandingCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Standing entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.competition:
                raise ValueError("Competition ID is required")
            if not item_data.equipe:
                raise ValueError("Team ID is required")

            db_standing = Standing(
                classement=item_data.classement,                id=item_data.id,                points_concedes=item_data.points_concedes,                points=item_data.points,                defaites=item_data.defaites,                matchs_joues=item_data.matchs_joues,                points_marques=item_data.points_marques,                victoires=item_data.victoires,                difference_points=item_data.difference_points,                nuls=item_data.nuls,                competition_id=item_data.competition,                equipe_id=item_data.equipe            )
            database.add(db_standing)
            database.flush()  # Get ID without committing
            created_items.append(db_standing.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Standing entities"
    }


@app.delete("/standing/bulk/", response_model=None, tags=["Standing"])
async def bulk_delete_standing(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Standing entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_standing = database.query(Standing).filter(Standing.id == item_id).first()
        if db_standing:
            database.delete(db_standing)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Standing entities"
    }

@app.put("/standing/{standing_id}/", response_model=None, tags=["Standing"])
async def update_standing(standing_id: int, standing_data: StandingCreate, database: Session = Depends(get_db)) -> Standing:
    db_standing = database.query(Standing).filter(Standing.id == standing_id).first()
    if db_standing is None:
        raise HTTPException(status_code=404, detail="Standing not found")

    setattr(db_standing, 'classement', standing_data.classement)
    setattr(db_standing, 'id', standing_data.id)
    setattr(db_standing, 'points_concedes', standing_data.points_concedes)
    setattr(db_standing, 'points', standing_data.points)
    setattr(db_standing, 'defaites', standing_data.defaites)
    setattr(db_standing, 'matchs_joues', standing_data.matchs_joues)
    setattr(db_standing, 'points_marques', standing_data.points_marques)
    setattr(db_standing, 'victoires', standing_data.victoires)
    setattr(db_standing, 'difference_points', standing_data.difference_points)
    setattr(db_standing, 'nuls', standing_data.nuls)
    if standing_data.competition is not None:
        db_competition = database.query(Competition).filter(Competition.id == standing_data.competition).first()
        if not db_competition:
            raise HTTPException(status_code=400, detail="Competition not found")
        setattr(db_standing, 'competition_id', standing_data.competition)
    if standing_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == standing_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
        setattr(db_standing, 'equipe_id', standing_data.equipe)
    database.commit()
    database.refresh(db_standing)

    return db_standing


@app.delete("/standing/{standing_id}/", response_model=None, tags=["Standing"])
async def delete_standing(standing_id: int, database: Session = Depends(get_db)):
    db_standing = database.query(Standing).filter(Standing.id == standing_id).first()
    if db_standing is None:
        raise HTTPException(status_code=404, detail="Standing not found")
    database.delete(db_standing)
    database.commit()
    return db_standing






############################################
#
#   PreMatchOdds functions
#
############################################

@app.get("/prematchodds/", response_model=None, tags=["PreMatchOdds"])
def get_all_prematchodds(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(PreMatchOdds)
        query = query.options(joinedload(PreMatchOdds.match))
        prematchodds_list = query.all()

        # Serialize with relationships included
        result = []
        for prematchodds_item in prematchodds_list:
            item_dict = prematchodds_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if prematchodds_item.match:
                related_obj = prematchodds_item.match
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['match'] = related_dict
            else:
                item_dict['match'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(PreMatchOdds).all()


@app.get("/prematchodds/count/", response_model=None, tags=["PreMatchOdds"])
def get_count_prematchodds(database: Session = Depends(get_db)) -> dict:
    """Get the total count of PreMatchOdds entities"""
    count = database.query(PreMatchOdds).count()
    return {"count": count}


@app.get("/prematchodds/paginated/", response_model=None, tags=["PreMatchOdds"])
def get_paginated_prematchodds(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of PreMatchOdds entities"""
    total = database.query(PreMatchOdds).count()
    prematchodds_list = database.query(PreMatchOdds).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": prematchodds_list
    }


@app.get("/prematchodds/search/", response_model=None, tags=["PreMatchOdds"])
def search_prematchodds(
    database: Session = Depends(get_db)
) -> list:
    """Search PreMatchOdds entities by attributes"""
    query = database.query(PreMatchOdds)


    results = query.all()
    return results


@app.get("/prematchodds/{prematchodds_id}/", response_model=None, tags=["PreMatchOdds"])
async def get_prematchodds(prematchodds_id: int, database: Session = Depends(get_db)) -> PreMatchOdds:
    db_prematchodds = database.query(PreMatchOdds).filter(PreMatchOdds.id == prematchodds_id).first()
    if db_prematchodds is None:
        raise HTTPException(status_code=404, detail="PreMatchOdds not found")

    response_data = {
        "prematchodds": db_prematchodds,
}
    return response_data



@app.post("/prematchodds/", response_model=None, tags=["PreMatchOdds"])
async def create_prematchodds(prematchodds_data: PreMatchOddsCreate, database: Session = Depends(get_db)) -> PreMatchOdds:

    if prematchodds_data.match is not None:
        db_match = database.query(Match).filter(Match.id == prematchodds_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
    else:
        raise HTTPException(status_code=400, detail="Match ID is required")

    db_prematchodds = PreMatchOdds(
        id=prematchodds_data.id,        pct_victoire_ext=prematchodds_data.pct_victoire_ext,        pct_victoire_dom=prematchodds_data.pct_victoire_dom,        source=prematchodds_data.source,        pct_match_nul=prematchodds_data.pct_match_nul,        updated_at=prematchodds_data.updated_at,        match_id=prematchodds_data.match        )

    database.add(db_prematchodds)
    database.commit()
    database.refresh(db_prematchodds)




    return db_prematchodds


@app.post("/prematchodds/bulk/", response_model=None, tags=["PreMatchOdds"])
async def bulk_create_prematchodds(items: list[PreMatchOddsCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple PreMatchOdds entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.match:
                raise ValueError("Match ID is required")

            db_prematchodds = PreMatchOdds(
                id=item_data.id,                pct_victoire_ext=item_data.pct_victoire_ext,                pct_victoire_dom=item_data.pct_victoire_dom,                source=item_data.source,                pct_match_nul=item_data.pct_match_nul,                updated_at=item_data.updated_at,                match_id=item_data.match            )
            database.add(db_prematchodds)
            database.flush()  # Get ID without committing
            created_items.append(db_prematchodds.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} PreMatchOdds entities"
    }


@app.delete("/prematchodds/bulk/", response_model=None, tags=["PreMatchOdds"])
async def bulk_delete_prematchodds(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple PreMatchOdds entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_prematchodds = database.query(PreMatchOdds).filter(PreMatchOdds.id == item_id).first()
        if db_prematchodds:
            database.delete(db_prematchodds)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} PreMatchOdds entities"
    }

@app.put("/prematchodds/{prematchodds_id}/", response_model=None, tags=["PreMatchOdds"])
async def update_prematchodds(prematchodds_id: int, prematchodds_data: PreMatchOddsCreate, database: Session = Depends(get_db)) -> PreMatchOdds:
    db_prematchodds = database.query(PreMatchOdds).filter(PreMatchOdds.id == prematchodds_id).first()
    if db_prematchodds is None:
        raise HTTPException(status_code=404, detail="PreMatchOdds not found")

    setattr(db_prematchodds, 'id', prematchodds_data.id)
    setattr(db_prematchodds, 'pct_victoire_ext', prematchodds_data.pct_victoire_ext)
    setattr(db_prematchodds, 'pct_victoire_dom', prematchodds_data.pct_victoire_dom)
    setattr(db_prematchodds, 'source', prematchodds_data.source)
    setattr(db_prematchodds, 'pct_match_nul', prematchodds_data.pct_match_nul)
    setattr(db_prematchodds, 'updated_at', prematchodds_data.updated_at)
    if prematchodds_data.match is not None:
        db_match = database.query(Match).filter(Match.id == prematchodds_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
        setattr(db_prematchodds, 'match_id', prematchodds_data.match)
    database.commit()
    database.refresh(db_prematchodds)

    return db_prematchodds


@app.delete("/prematchodds/{prematchodds_id}/", response_model=None, tags=["PreMatchOdds"])
async def delete_prematchodds(prematchodds_id: int, database: Session = Depends(get_db)):
    db_prematchodds = database.query(PreMatchOdds).filter(PreMatchOdds.id == prematchodds_id).first()
    if db_prematchodds is None:
        raise HTTPException(status_code=404, detail="PreMatchOdds not found")
    database.delete(db_prematchodds)
    database.commit()
    return db_prematchodds






############################################
#
#   Sport functions
#
############################################

@app.get("/sport/", response_model=None, tags=["Sport"])
def get_all_sport(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Sport)
        sport_list = query.all()

        # Serialize with relationships included
        result = []
        for sport_item in sport_list:
            item_dict = sport_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            competition_list = database.query(Competition).filter(Competition.sport_id == sport_item.id).all()
            item_dict['competitions'] = []
            for competition_obj in competition_list:
                competition_dict = competition_obj.__dict__.copy()
                competition_dict.pop('_sa_instance_state', None)
                item_dict['competitions'].append(competition_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Sport).all()


@app.get("/sport/count/", response_model=None, tags=["Sport"])
def get_count_sport(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Sport entities"""
    count = database.query(Sport).count()
    return {"count": count}


@app.get("/sport/paginated/", response_model=None, tags=["Sport"])
def get_paginated_sport(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Sport entities"""
    total = database.query(Sport).count()
    sport_list = database.query(Sport).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": sport_list
        }

    result = []
    for sport_item in sport_list:
        competitions_ids = database.query(Competition.id).filter(Competition.sport_id == sport_item.id).all()
        item_data = {
            "sport": sport_item,
            "competitions_ids": [x[0] for x in competitions_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/sport/search/", response_model=None, tags=["Sport"])
def search_sport(
    database: Session = Depends(get_db)
) -> list:
    """Search Sport entities by attributes"""
    query = database.query(Sport)


    results = query.all()
    return results


@app.get("/sport/{sport_id}/", response_model=None, tags=["Sport"])
async def get_sport(sport_id: int, database: Session = Depends(get_db)) -> Sport:
    db_sport = database.query(Sport).filter(Sport.id == sport_id).first()
    if db_sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")

    competitions_ids = database.query(Competition.id).filter(Competition.sport_id == db_sport.id).all()
    response_data = {
        "sport": db_sport,
        "competitions_ids": [x[0] for x in competitions_ids]}
    return response_data



@app.post("/sport/", response_model=None, tags=["Sport"])
async def create_sport(sport_data: SportCreate, database: Session = Depends(get_db)) -> Sport:


    db_sport = Sport(
        id=sport_data.id,        logo_url=sport_data.logo_url,        description=sport_data.description,        nom=sport_data.nom,        type=sport_data.type.value        )

    database.add(db_sport)
    database.commit()
    database.refresh(db_sport)

    if sport_data.competitions:
        # Validate that all Competition IDs exist
        for competition_id in sport_data.competitions:
            db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
            if not db_competition:
                raise HTTPException(status_code=400, detail=f"Competition with id {competition_id} not found")

        # Update the related entities with the new foreign key
        database.query(Competition).filter(Competition.id.in_(sport_data.competitions)).update(
            {Competition.sport_id: db_sport.id}, synchronize_session=False
        )
        database.commit()



    competitions_ids = database.query(Competition.id).filter(Competition.sport_id == db_sport.id).all()
    response_data = {
        "sport": db_sport,
        "competitions_ids": [x[0] for x in competitions_ids]    }
    return response_data


@app.post("/sport/bulk/", response_model=None, tags=["Sport"])
async def bulk_create_sport(items: list[SportCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Sport entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_sport = Sport(
                id=item_data.id,                logo_url=item_data.logo_url,                description=item_data.description,                nom=item_data.nom,                type=item_data.type.value            )
            database.add(db_sport)
            database.flush()  # Get ID without committing
            created_items.append(db_sport.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Sport entities"
    }


@app.delete("/sport/bulk/", response_model=None, tags=["Sport"])
async def bulk_delete_sport(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Sport entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_sport = database.query(Sport).filter(Sport.id == item_id).first()
        if db_sport:
            database.delete(db_sport)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Sport entities"
    }

@app.put("/sport/{sport_id}/", response_model=None, tags=["Sport"])
async def update_sport(sport_id: int, sport_data: SportCreate, database: Session = Depends(get_db)) -> Sport:
    db_sport = database.query(Sport).filter(Sport.id == sport_id).first()
    if db_sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")

    setattr(db_sport, 'id', sport_data.id)
    setattr(db_sport, 'logo_url', sport_data.logo_url)
    setattr(db_sport, 'description', sport_data.description)
    setattr(db_sport, 'nom', sport_data.nom)
    setattr(db_sport, 'type', sport_data.type.value)
    if sport_data.competitions is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Competition).filter(Competition.sport_id == db_sport.id).update(
            {Competition.sport_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if sport_data.competitions:
            # Validate that all IDs exist
            for competition_id in sport_data.competitions:
                db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
                if not db_competition:
                    raise HTTPException(status_code=400, detail=f"Competition with id {competition_id} not found")

            # Update the related entities with the new foreign key
            database.query(Competition).filter(Competition.id.in_(sport_data.competitions)).update(
                {Competition.sport_id: db_sport.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_sport)

    competitions_ids = database.query(Competition.id).filter(Competition.sport_id == db_sport.id).all()
    response_data = {
        "sport": db_sport,
        "competitions_ids": [x[0] for x in competitions_ids]    }
    return response_data


@app.delete("/sport/{sport_id}/", response_model=None, tags=["Sport"])
async def delete_sport(sport_id: int, database: Session = Depends(get_db)):
    db_sport = database.query(Sport).filter(Sport.id == sport_id).first()
    if db_sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")
    database.delete(db_sport)
    database.commit()
    return db_sport


@app.get("/sport/{sport_id}/competitions/", response_model=None, tags=["Sport Relationships"])
async def get_competitions_of_sport(sport_id: int, database: Session = Depends(get_db)):
    """Get all Competition entities related to this Sport through competitions"""
    db_sport = database.query(Sport).filter(Sport.id == sport_id).first()
    if db_sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")

    competitions_list = database.query(Competition).filter(Competition.sport_id == sport_id).all()

    return {
        "sport_id": sport_id,
        "competitions_count": len(competitions_list),
        "competitions": competitions_list
    }





############################################
#
#   LineupPlayer functions
#
############################################

@app.get("/lineupplayer/", response_model=None, tags=["LineupPlayer"])
def get_all_lineupplayer(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(LineupPlayer)
        query = query.options(joinedload(LineupPlayer.joueur))
        query = query.options(joinedload(LineupPlayer.lineup))
        lineupplayer_list = query.all()

        # Serialize with relationships included
        result = []
        for lineupplayer_item in lineupplayer_list:
            item_dict = lineupplayer_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if lineupplayer_item.joueur:
                related_obj = lineupplayer_item.joueur
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['joueur'] = related_dict
            else:
                item_dict['joueur'] = None
            if lineupplayer_item.lineup:
                related_obj = lineupplayer_item.lineup
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['lineup'] = related_dict
            else:
                item_dict['lineup'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(LineupPlayer).all()


@app.get("/lineupplayer/count/", response_model=None, tags=["LineupPlayer"])
def get_count_lineupplayer(database: Session = Depends(get_db)) -> dict:
    """Get the total count of LineupPlayer entities"""
    count = database.query(LineupPlayer).count()
    return {"count": count}


@app.get("/lineupplayer/paginated/", response_model=None, tags=["LineupPlayer"])
def get_paginated_lineupplayer(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of LineupPlayer entities"""
    total = database.query(LineupPlayer).count()
    lineupplayer_list = database.query(LineupPlayer).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": lineupplayer_list
    }


@app.get("/lineupplayer/search/", response_model=None, tags=["LineupPlayer"])
def search_lineupplayer(
    database: Session = Depends(get_db)
) -> list:
    """Search LineupPlayer entities by attributes"""
    query = database.query(LineupPlayer)


    results = query.all()
    return results


@app.get("/lineupplayer/{lineupplayer_id}/", response_model=None, tags=["LineupPlayer"])
async def get_lineupplayer(lineupplayer_id: int, database: Session = Depends(get_db)) -> LineupPlayer:
    db_lineupplayer = database.query(LineupPlayer).filter(LineupPlayer.id == lineupplayer_id).first()
    if db_lineupplayer is None:
        raise HTTPException(status_code=404, detail="LineupPlayer not found")

    response_data = {
        "lineupplayer": db_lineupplayer,
}
    return response_data



@app.post("/lineupplayer/", response_model=None, tags=["LineupPlayer"])
async def create_lineupplayer(lineupplayer_data: LineupPlayerCreate, database: Session = Depends(get_db)) -> LineupPlayer:

    if lineupplayer_data.joueur is not None:
        db_joueur = database.query(Player).filter(Player.id == lineupplayer_data.joueur).first()
        if not db_joueur:
            raise HTTPException(status_code=400, detail="Player not found")
    else:
        raise HTTPException(status_code=400, detail="Player ID is required")
    if lineupplayer_data.lineup is not None:
        db_lineup = database.query(Lineup).filter(Lineup.id == lineupplayer_data.lineup).first()
        if not db_lineup:
            raise HTTPException(status_code=400, detail="Lineup not found")
    else:
        raise HTTPException(status_code=400, detail="Lineup ID is required")

    db_lineupplayer = LineupPlayer(
        position_match=lineupplayer_data.position_match,        est_capitaine=lineupplayer_data.est_capitaine,        numero_maillot=lineupplayer_data.numero_maillot,        ordre_entree=lineupplayer_data.ordre_entree,        id=lineupplayer_data.id,        est_titulaire=lineupplayer_data.est_titulaire,        joueur_id=lineupplayer_data.joueur,        lineup_id=lineupplayer_data.lineup        )

    database.add(db_lineupplayer)
    database.commit()
    database.refresh(db_lineupplayer)




    return db_lineupplayer


@app.post("/lineupplayer/bulk/", response_model=None, tags=["LineupPlayer"])
async def bulk_create_lineupplayer(items: list[LineupPlayerCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple LineupPlayer entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.joueur:
                raise ValueError("Player ID is required")
            if not item_data.lineup:
                raise ValueError("Lineup ID is required")

            db_lineupplayer = LineupPlayer(
                position_match=item_data.position_match,                est_capitaine=item_data.est_capitaine,                numero_maillot=item_data.numero_maillot,                ordre_entree=item_data.ordre_entree,                id=item_data.id,                est_titulaire=item_data.est_titulaire,                joueur_id=item_data.joueur,                lineup_id=item_data.lineup            )
            database.add(db_lineupplayer)
            database.flush()  # Get ID without committing
            created_items.append(db_lineupplayer.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} LineupPlayer entities"
    }


@app.delete("/lineupplayer/bulk/", response_model=None, tags=["LineupPlayer"])
async def bulk_delete_lineupplayer(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple LineupPlayer entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_lineupplayer = database.query(LineupPlayer).filter(LineupPlayer.id == item_id).first()
        if db_lineupplayer:
            database.delete(db_lineupplayer)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} LineupPlayer entities"
    }

@app.put("/lineupplayer/{lineupplayer_id}/", response_model=None, tags=["LineupPlayer"])
async def update_lineupplayer(lineupplayer_id: int, lineupplayer_data: LineupPlayerCreate, database: Session = Depends(get_db)) -> LineupPlayer:
    db_lineupplayer = database.query(LineupPlayer).filter(LineupPlayer.id == lineupplayer_id).first()
    if db_lineupplayer is None:
        raise HTTPException(status_code=404, detail="LineupPlayer not found")

    setattr(db_lineupplayer, 'position_match', lineupplayer_data.position_match)
    setattr(db_lineupplayer, 'est_capitaine', lineupplayer_data.est_capitaine)
    setattr(db_lineupplayer, 'numero_maillot', lineupplayer_data.numero_maillot)
    setattr(db_lineupplayer, 'ordre_entree', lineupplayer_data.ordre_entree)
    setattr(db_lineupplayer, 'id', lineupplayer_data.id)
    setattr(db_lineupplayer, 'est_titulaire', lineupplayer_data.est_titulaire)
    if lineupplayer_data.joueur is not None:
        db_joueur = database.query(Player).filter(Player.id == lineupplayer_data.joueur).first()
        if not db_joueur:
            raise HTTPException(status_code=400, detail="Player not found")
        setattr(db_lineupplayer, 'joueur_id', lineupplayer_data.joueur)
    if lineupplayer_data.lineup is not None:
        db_lineup = database.query(Lineup).filter(Lineup.id == lineupplayer_data.lineup).first()
        if not db_lineup:
            raise HTTPException(status_code=400, detail="Lineup not found")
        setattr(db_lineupplayer, 'lineup_id', lineupplayer_data.lineup)
    database.commit()
    database.refresh(db_lineupplayer)

    return db_lineupplayer


@app.delete("/lineupplayer/{lineupplayer_id}/", response_model=None, tags=["LineupPlayer"])
async def delete_lineupplayer(lineupplayer_id: int, database: Session = Depends(get_db)):
    db_lineupplayer = database.query(LineupPlayer).filter(LineupPlayer.id == lineupplayer_id).first()
    if db_lineupplayer is None:
        raise HTTPException(status_code=404, detail="LineupPlayer not found")
    database.delete(db_lineupplayer)
    database.commit()
    return db_lineupplayer






############################################
#
#   Reaction functions
#
############################################

@app.get("/reaction/", response_model=None, tags=["Reaction"])
def get_all_reaction(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Reaction)
        query = query.options(joinedload(Reaction.user))
        query = query.options(joinedload(Reaction.message))
        reaction_list = query.all()

        # Serialize with relationships included
        result = []
        for reaction_item in reaction_list:
            item_dict = reaction_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if reaction_item.user:
                related_obj = reaction_item.user
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['user'] = related_dict
            else:
                item_dict['user'] = None
            if reaction_item.message:
                related_obj = reaction_item.message
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['message'] = related_dict
            else:
                item_dict['message'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Reaction).all()


@app.get("/reaction/count/", response_model=None, tags=["Reaction"])
def get_count_reaction(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Reaction entities"""
    count = database.query(Reaction).count()
    return {"count": count}


@app.get("/reaction/paginated/", response_model=None, tags=["Reaction"])
def get_paginated_reaction(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Reaction entities"""
    total = database.query(Reaction).count()
    reaction_list = database.query(Reaction).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": reaction_list
    }


@app.get("/reaction/search/", response_model=None, tags=["Reaction"])
def search_reaction(
    database: Session = Depends(get_db)
) -> list:
    """Search Reaction entities by attributes"""
    query = database.query(Reaction)


    results = query.all()
    return results


@app.get("/reaction/{reaction_id}/", response_model=None, tags=["Reaction"])
async def get_reaction(reaction_id: int, database: Session = Depends(get_db)) -> Reaction:
    db_reaction = database.query(Reaction).filter(Reaction.id == reaction_id).first()
    if db_reaction is None:
        raise HTTPException(status_code=404, detail="Reaction not found")

    response_data = {
        "reaction": db_reaction,
}
    return response_data



@app.post("/reaction/", response_model=None, tags=["Reaction"])
async def create_reaction(reaction_data: ReactionCreate, database: Session = Depends(get_db)) -> Reaction:

    if reaction_data.user is not None:
        db_user = database.query(User).filter(User.id == reaction_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if reaction_data.message is not None:
        db_message = database.query(Message).filter(Message.id == reaction_data.message).first()
        if not db_message:
            raise HTTPException(status_code=400, detail="Message not found")
    else:
        raise HTTPException(status_code=400, detail="Message ID is required")

    db_reaction = Reaction(
        type=reaction_data.type.value,        id=reaction_data.id,        created_at=reaction_data.created_at,        user_id=reaction_data.user,        message_id=reaction_data.message        )

    database.add(db_reaction)
    database.commit()
    database.refresh(db_reaction)




    return db_reaction


@app.post("/reaction/bulk/", response_model=None, tags=["Reaction"])
async def bulk_create_reaction(items: list[ReactionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Reaction entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.user:
                raise ValueError("User ID is required")
            if not item_data.message:
                raise ValueError("Message ID is required")

            db_reaction = Reaction(
                type=item_data.type.value,                id=item_data.id,                created_at=item_data.created_at,                user_id=item_data.user,                message_id=item_data.message            )
            database.add(db_reaction)
            database.flush()  # Get ID without committing
            created_items.append(db_reaction.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Reaction entities"
    }


@app.delete("/reaction/bulk/", response_model=None, tags=["Reaction"])
async def bulk_delete_reaction(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Reaction entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_reaction = database.query(Reaction).filter(Reaction.id == item_id).first()
        if db_reaction:
            database.delete(db_reaction)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Reaction entities"
    }

@app.put("/reaction/{reaction_id}/", response_model=None, tags=["Reaction"])
async def update_reaction(reaction_id: int, reaction_data: ReactionCreate, database: Session = Depends(get_db)) -> Reaction:
    db_reaction = database.query(Reaction).filter(Reaction.id == reaction_id).first()
    if db_reaction is None:
        raise HTTPException(status_code=404, detail="Reaction not found")

    setattr(db_reaction, 'type', reaction_data.type.value)
    setattr(db_reaction, 'id', reaction_data.id)
    setattr(db_reaction, 'created_at', reaction_data.created_at)
    if reaction_data.user is not None:
        db_user = database.query(User).filter(User.id == reaction_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_reaction, 'user_id', reaction_data.user)
    if reaction_data.message is not None:
        db_message = database.query(Message).filter(Message.id == reaction_data.message).first()
        if not db_message:
            raise HTTPException(status_code=400, detail="Message not found")
        setattr(db_reaction, 'message_id', reaction_data.message)
    database.commit()
    database.refresh(db_reaction)

    return db_reaction


@app.delete("/reaction/{reaction_id}/", response_model=None, tags=["Reaction"])
async def delete_reaction(reaction_id: int, database: Session = Depends(get_db)):
    db_reaction = database.query(Reaction).filter(Reaction.id == reaction_id).first()
    if db_reaction is None:
        raise HTTPException(status_code=404, detail="Reaction not found")
    database.delete(db_reaction)
    database.commit()
    return db_reaction






############################################
#
#   Lineup functions
#
############################################

@app.get("/lineup/", response_model=None, tags=["Lineup"])
def get_all_lineup(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Lineup)
        query = query.options(joinedload(Lineup.equipe))
        query = query.options(joinedload(Lineup.match))
        lineup_list = query.all()

        # Serialize with relationships included
        result = []
        for lineup_item in lineup_list:
            item_dict = lineup_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if lineup_item.equipe:
                related_obj = lineup_item.equipe
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['equipe'] = related_dict
            else:
                item_dict['equipe'] = None
            if lineup_item.match:
                related_obj = lineup_item.match
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['match'] = related_dict
            else:
                item_dict['match'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            lineupplayer_list = database.query(LineupPlayer).filter(LineupPlayer.lineup_id == lineup_item.id).all()
            item_dict['joueurs'] = []
            for lineupplayer_obj in lineupplayer_list:
                lineupplayer_dict = lineupplayer_obj.__dict__.copy()
                lineupplayer_dict.pop('_sa_instance_state', None)
                item_dict['joueurs'].append(lineupplayer_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Lineup).all()


@app.get("/lineup/count/", response_model=None, tags=["Lineup"])
def get_count_lineup(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Lineup entities"""
    count = database.query(Lineup).count()
    return {"count": count}


@app.get("/lineup/paginated/", response_model=None, tags=["Lineup"])
def get_paginated_lineup(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Lineup entities"""
    total = database.query(Lineup).count()
    lineup_list = database.query(Lineup).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": lineup_list
        }

    result = []
    for lineup_item in lineup_list:
        joueurs_ids = database.query(LineupPlayer.id).filter(LineupPlayer.lineup_id == lineup_item.id).all()
        item_data = {
            "lineup": lineup_item,
            "joueurs_ids": [x[0] for x in joueurs_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/lineup/search/", response_model=None, tags=["Lineup"])
def search_lineup(
    database: Session = Depends(get_db)
) -> list:
    """Search Lineup entities by attributes"""
    query = database.query(Lineup)


    results = query.all()
    return results


@app.get("/lineup/{lineup_id}/", response_model=None, tags=["Lineup"])
async def get_lineup(lineup_id: int, database: Session = Depends(get_db)) -> Lineup:
    db_lineup = database.query(Lineup).filter(Lineup.id == lineup_id).first()
    if db_lineup is None:
        raise HTTPException(status_code=404, detail="Lineup not found")

    joueurs_ids = database.query(LineupPlayer.id).filter(LineupPlayer.lineup_id == db_lineup.id).all()
    response_data = {
        "lineup": db_lineup,
        "joueurs_ids": [x[0] for x in joueurs_ids]}
    return response_data



@app.post("/lineup/", response_model=None, tags=["Lineup"])
async def create_lineup(lineup_data: LineupCreate, database: Session = Depends(get_db)) -> Lineup:

    if lineup_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == lineup_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
    else:
        raise HTTPException(status_code=400, detail="Team ID is required")
    if lineup_data.match is not None:
        db_match = database.query(Match).filter(Match.id == lineup_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
    else:
        raise HTTPException(status_code=400, detail="Match ID is required")

    db_lineup = Lineup(
        statut=lineup_data.statut.value,        id=lineup_data.id,        role_double=lineup_data.role_double,        publiee_le=lineup_data.publiee_le,        formation=lineup_data.formation,        est_domicile=lineup_data.est_domicile,        equipe_id=lineup_data.equipe,        match_id=lineup_data.match        )

    database.add(db_lineup)
    database.commit()
    database.refresh(db_lineup)

    if lineup_data.joueurs:
        # Validate that all LineupPlayer IDs exist
        for lineupplayer_id in lineup_data.joueurs:
            db_lineupplayer = database.query(LineupPlayer).filter(LineupPlayer.id == lineupplayer_id).first()
            if not db_lineupplayer:
                raise HTTPException(status_code=400, detail=f"LineupPlayer with id {lineupplayer_id} not found")

        # Update the related entities with the new foreign key
        database.query(LineupPlayer).filter(LineupPlayer.id.in_(lineup_data.joueurs)).update(
            {LineupPlayer.lineup_id: db_lineup.id}, synchronize_session=False
        )
        database.commit()



    joueurs_ids = database.query(LineupPlayer.id).filter(LineupPlayer.lineup_id == db_lineup.id).all()
    response_data = {
        "lineup": db_lineup,
        "joueurs_ids": [x[0] for x in joueurs_ids]    }
    return response_data


@app.post("/lineup/bulk/", response_model=None, tags=["Lineup"])
async def bulk_create_lineup(items: list[LineupCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Lineup entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.equipe:
                raise ValueError("Team ID is required")
            if not item_data.match:
                raise ValueError("Match ID is required")

            db_lineup = Lineup(
                statut=item_data.statut.value,                id=item_data.id,                role_double=item_data.role_double,                publiee_le=item_data.publiee_le,                formation=item_data.formation,                est_domicile=item_data.est_domicile,                equipe_id=item_data.equipe,                match_id=item_data.match            )
            database.add(db_lineup)
            database.flush()  # Get ID without committing
            created_items.append(db_lineup.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Lineup entities"
    }


@app.delete("/lineup/bulk/", response_model=None, tags=["Lineup"])
async def bulk_delete_lineup(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Lineup entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_lineup = database.query(Lineup).filter(Lineup.id == item_id).first()
        if db_lineup:
            database.delete(db_lineup)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Lineup entities"
    }

@app.put("/lineup/{lineup_id}/", response_model=None, tags=["Lineup"])
async def update_lineup(lineup_id: int, lineup_data: LineupCreate, database: Session = Depends(get_db)) -> Lineup:
    db_lineup = database.query(Lineup).filter(Lineup.id == lineup_id).first()
    if db_lineup is None:
        raise HTTPException(status_code=404, detail="Lineup not found")

    setattr(db_lineup, 'statut', lineup_data.statut.value)
    setattr(db_lineup, 'id', lineup_data.id)
    setattr(db_lineup, 'role_double', lineup_data.role_double)
    setattr(db_lineup, 'publiee_le', lineup_data.publiee_le)
    setattr(db_lineup, 'formation', lineup_data.formation)
    setattr(db_lineup, 'est_domicile', lineup_data.est_domicile)
    if lineup_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == lineup_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
        setattr(db_lineup, 'equipe_id', lineup_data.equipe)
    if lineup_data.match is not None:
        db_match = database.query(Match).filter(Match.id == lineup_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
        setattr(db_lineup, 'match_id', lineup_data.match)
    if lineup_data.joueurs is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(LineupPlayer).filter(LineupPlayer.lineup_id == db_lineup.id).update(
            {LineupPlayer.lineup_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if lineup_data.joueurs:
            # Validate that all IDs exist
            for lineupplayer_id in lineup_data.joueurs:
                db_lineupplayer = database.query(LineupPlayer).filter(LineupPlayer.id == lineupplayer_id).first()
                if not db_lineupplayer:
                    raise HTTPException(status_code=400, detail=f"LineupPlayer with id {lineupplayer_id} not found")

            # Update the related entities with the new foreign key
            database.query(LineupPlayer).filter(LineupPlayer.id.in_(lineup_data.joueurs)).update(
                {LineupPlayer.lineup_id: db_lineup.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_lineup)

    joueurs_ids = database.query(LineupPlayer.id).filter(LineupPlayer.lineup_id == db_lineup.id).all()
    response_data = {
        "lineup": db_lineup,
        "joueurs_ids": [x[0] for x in joueurs_ids]    }
    return response_data


@app.delete("/lineup/{lineup_id}/", response_model=None, tags=["Lineup"])
async def delete_lineup(lineup_id: int, database: Session = Depends(get_db)):
    db_lineup = database.query(Lineup).filter(Lineup.id == lineup_id).first()
    if db_lineup is None:
        raise HTTPException(status_code=404, detail="Lineup not found")
    database.delete(db_lineup)
    database.commit()
    return db_lineup


@app.get("/lineup/{lineup_id}/joueurs/", response_model=None, tags=["Lineup Relationships"])
async def get_joueurs_of_lineup(lineup_id: int, database: Session = Depends(get_db)):
    """Get all LineupPlayer entities related to this Lineup through joueurs"""
    db_lineup = database.query(Lineup).filter(Lineup.id == lineup_id).first()
    if db_lineup is None:
        raise HTTPException(status_code=404, detail="Lineup not found")

    joueurs_list = database.query(LineupPlayer).filter(LineupPlayer.lineup_id == lineup_id).all()

    return {
        "lineup_id": lineup_id,
        "joueurs_count": len(joueurs_list),
        "joueurs": joueurs_list
    }





############################################
#
#   Player functions
#
############################################

@app.get("/player/", response_model=None, tags=["Player"])
def get_all_player(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Player)
        query = query.options(joinedload(Player.joueur))
        query = query.options(joinedload(Player.equipe))
        player_list = query.all()

        # Serialize with relationships included
        result = []
        for player_item in player_list:
            item_dict = player_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if player_item.joueur:
                related_obj = player_item.joueur
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['joueur'] = related_dict
            else:
                item_dict['joueur'] = None
            if player_item.equipe:
                related_obj = player_item.equipe
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['equipe'] = related_dict
            else:
                item_dict['equipe'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            lineupplayer_list = database.query(LineupPlayer).filter(LineupPlayer.joueur_id == player_item.id).all()
            item_dict['apparitions'] = []
            for lineupplayer_obj in lineupplayer_list:
                lineupplayer_dict = lineupplayer_obj.__dict__.copy()
                lineupplayer_dict.pop('_sa_instance_state', None)
                item_dict['apparitions'].append(lineupplayer_dict)
            matchevent_list = database.query(MatchEvent).filter(MatchEvent.joueur_id == player_item.id).all()
            item_dict['evenements_joues'] = []
            for matchevent_obj in matchevent_list:
                matchevent_dict = matchevent_obj.__dict__.copy()
                matchevent_dict.pop('_sa_instance_state', None)
                item_dict['evenements_joues'].append(matchevent_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Player).all()


@app.get("/player/count/", response_model=None, tags=["Player"])
def get_count_player(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Player entities"""
    count = database.query(Player).count()
    return {"count": count}


@app.get("/player/paginated/", response_model=None, tags=["Player"])
def get_paginated_player(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Player entities"""
    total = database.query(Player).count()
    player_list = database.query(Player).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": player_list
        }

    result = []
    for player_item in player_list:
        apparitions_ids = database.query(LineupPlayer.id).filter(LineupPlayer.joueur_id == player_item.id).all()
        evenements_joues_ids = database.query(MatchEvent.id).filter(MatchEvent.joueur_id == player_item.id).all()
        item_data = {
            "player": player_item,
            "apparitions_ids": [x[0] for x in apparitions_ids],            "evenements_joues_ids": [x[0] for x in evenements_joues_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/player/search/", response_model=None, tags=["Player"])
def search_player(
    database: Session = Depends(get_db)
) -> list:
    """Search Player entities by attributes"""
    query = database.query(Player)


    results = query.all()
    return results


@app.get("/player/{player_id}/", response_model=None, tags=["Player"])
async def get_player(player_id: int, database: Session = Depends(get_db)) -> Player:
    db_player = database.query(Player).filter(Player.id == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    apparitions_ids = database.query(LineupPlayer.id).filter(LineupPlayer.joueur_id == db_player.id).all()
    evenements_joues_ids = database.query(MatchEvent.id).filter(MatchEvent.joueur_id == db_player.id).all()
    response_data = {
        "player": db_player,
        "apparitions_ids": [x[0] for x in apparitions_ids],        "evenements_joues_ids": [x[0] for x in evenements_joues_ids]}
    return response_data



@app.post("/player/", response_model=None, tags=["Player"])
async def create_player(player_data: PlayerCreate, database: Session = Depends(get_db)) -> Player:

    if player_data.joueur is not None:
        db_joueur = database.query(FavoritePlayer).filter(FavoritePlayer.id == player_data.joueur).first()
        if not db_joueur:
            raise HTTPException(status_code=400, detail="FavoritePlayer not found")
    else:
        raise HTTPException(status_code=400, detail="FavoritePlayer ID is required")
    if player_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == player_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
    else:
        raise HTTPException(status_code=400, detail="Team ID is required")

    db_player = Player(
        nom=player_data.nom,        prenom=player_data.prenom,        id=player_data.id,        numero=player_data.numero,        nationalite=player_data.nationalite,        date_naissance=player_data.date_naissance,        photo_url=player_data.photo_url,        position=player_data.position.value,        joueur_id=player_data.joueur,        equipe_id=player_data.equipe        )

    database.add(db_player)
    database.commit()
    database.refresh(db_player)

    if player_data.apparitions:
        # Validate that all LineupPlayer IDs exist
        for lineupplayer_id in player_data.apparitions:
            db_lineupplayer = database.query(LineupPlayer).filter(LineupPlayer.id == lineupplayer_id).first()
            if not db_lineupplayer:
                raise HTTPException(status_code=400, detail=f"LineupPlayer with id {lineupplayer_id} not found")

        # Update the related entities with the new foreign key
        database.query(LineupPlayer).filter(LineupPlayer.id.in_(player_data.apparitions)).update(
            {LineupPlayer.joueur_id: db_player.id}, synchronize_session=False
        )
        database.commit()
    if player_data.evenements_joues:
        # Validate that all MatchEvent IDs exist
        for matchevent_id in player_data.evenements_joues:
            db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
            if not db_matchevent:
                raise HTTPException(status_code=400, detail=f"MatchEvent with id {matchevent_id} not found")

        # Update the related entities with the new foreign key
        database.query(MatchEvent).filter(MatchEvent.id.in_(player_data.evenements_joues)).update(
            {MatchEvent.joueur_id: db_player.id}, synchronize_session=False
        )
        database.commit()



    apparitions_ids = database.query(LineupPlayer.id).filter(LineupPlayer.joueur_id == db_player.id).all()
    evenements_joues_ids = database.query(MatchEvent.id).filter(MatchEvent.joueur_id == db_player.id).all()
    response_data = {
        "player": db_player,
        "apparitions_ids": [x[0] for x in apparitions_ids],        "evenements_joues_ids": [x[0] for x in evenements_joues_ids]    }
    return response_data


@app.post("/player/bulk/", response_model=None, tags=["Player"])
async def bulk_create_player(items: list[PlayerCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Player entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.joueur:
                raise ValueError("FavoritePlayer ID is required")
            if not item_data.equipe:
                raise ValueError("Team ID is required")

            db_player = Player(
                nom=item_data.nom,                prenom=item_data.prenom,                id=item_data.id,                numero=item_data.numero,                nationalite=item_data.nationalite,                date_naissance=item_data.date_naissance,                photo_url=item_data.photo_url,                position=item_data.position.value,                joueur_id=item_data.joueur,                equipe_id=item_data.equipe            )
            database.add(db_player)
            database.flush()  # Get ID without committing
            created_items.append(db_player.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Player entities"
    }


@app.delete("/player/bulk/", response_model=None, tags=["Player"])
async def bulk_delete_player(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Player entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_player = database.query(Player).filter(Player.id == item_id).first()
        if db_player:
            database.delete(db_player)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Player entities"
    }

@app.put("/player/{player_id}/", response_model=None, tags=["Player"])
async def update_player(player_id: int, player_data: PlayerCreate, database: Session = Depends(get_db)) -> Player:
    db_player = database.query(Player).filter(Player.id == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    setattr(db_player, 'nom', player_data.nom)
    setattr(db_player, 'prenom', player_data.prenom)
    setattr(db_player, 'id', player_data.id)
    setattr(db_player, 'numero', player_data.numero)
    setattr(db_player, 'nationalite', player_data.nationalite)
    setattr(db_player, 'date_naissance', player_data.date_naissance)
    setattr(db_player, 'photo_url', player_data.photo_url)
    setattr(db_player, 'position', player_data.position.value)
    if player_data.joueur is not None:
        db_joueur = database.query(FavoritePlayer).filter(FavoritePlayer.id == player_data.joueur).first()
        if not db_joueur:
            raise HTTPException(status_code=400, detail="FavoritePlayer not found")
        setattr(db_player, 'joueur_id', player_data.joueur)
    if player_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == player_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
        setattr(db_player, 'equipe_id', player_data.equipe)
    if player_data.apparitions is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(LineupPlayer).filter(LineupPlayer.joueur_id == db_player.id).update(
            {LineupPlayer.joueur_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if player_data.apparitions:
            # Validate that all IDs exist
            for lineupplayer_id in player_data.apparitions:
                db_lineupplayer = database.query(LineupPlayer).filter(LineupPlayer.id == lineupplayer_id).first()
                if not db_lineupplayer:
                    raise HTTPException(status_code=400, detail=f"LineupPlayer with id {lineupplayer_id} not found")

            # Update the related entities with the new foreign key
            database.query(LineupPlayer).filter(LineupPlayer.id.in_(player_data.apparitions)).update(
                {LineupPlayer.joueur_id: db_player.id}, synchronize_session=False
            )
    if player_data.evenements_joues is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(MatchEvent).filter(MatchEvent.joueur_id == db_player.id).update(
            {MatchEvent.joueur_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if player_data.evenements_joues:
            # Validate that all IDs exist
            for matchevent_id in player_data.evenements_joues:
                db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
                if not db_matchevent:
                    raise HTTPException(status_code=400, detail=f"MatchEvent with id {matchevent_id} not found")

            # Update the related entities with the new foreign key
            database.query(MatchEvent).filter(MatchEvent.id.in_(player_data.evenements_joues)).update(
                {MatchEvent.joueur_id: db_player.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_player)

    apparitions_ids = database.query(LineupPlayer.id).filter(LineupPlayer.joueur_id == db_player.id).all()
    evenements_joues_ids = database.query(MatchEvent.id).filter(MatchEvent.joueur_id == db_player.id).all()
    response_data = {
        "player": db_player,
        "apparitions_ids": [x[0] for x in apparitions_ids],        "evenements_joues_ids": [x[0] for x in evenements_joues_ids]    }
    return response_data


@app.delete("/player/{player_id}/", response_model=None, tags=["Player"])
async def delete_player(player_id: int, database: Session = Depends(get_db)):
    db_player = database.query(Player).filter(Player.id == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    database.delete(db_player)
    database.commit()
    return db_player


@app.get("/player/{player_id}/apparitions/", response_model=None, tags=["Player Relationships"])
async def get_apparitions_of_player(player_id: int, database: Session = Depends(get_db)):
    """Get all LineupPlayer entities related to this Player through apparitions"""
    db_player = database.query(Player).filter(Player.id == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    apparitions_list = database.query(LineupPlayer).filter(LineupPlayer.joueur_id == player_id).all()

    return {
        "player_id": player_id,
        "apparitions_count": len(apparitions_list),
        "apparitions": apparitions_list
    }

@app.get("/player/{player_id}/evenements_joues/", response_model=None, tags=["Player Relationships"])
async def get_evenements_joues_of_player(player_id: int, database: Session = Depends(get_db)):
    """Get all MatchEvent entities related to this Player through evenements_joues"""
    db_player = database.query(Player).filter(Player.id == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    evenements_joues_list = database.query(MatchEvent).filter(MatchEvent.joueur_id == player_id).all()

    return {
        "player_id": player_id,
        "evenements_joues_count": len(evenements_joues_list),
        "evenements_joues": evenements_joues_list
    }





############################################
#
#   Stadium functions
#
############################################

@app.get("/stadium/", response_model=None, tags=["Stadium"])
def get_all_stadium(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Stadium)
        stadium_list = query.all()

        # Serialize with relationships included
        result = []
        for stadium_item in stadium_list:
            item_dict = stadium_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            team_list = database.query(Team).filter(Team.stade_domicile_id == stadium_item.id).all()
            item_dict['equipes_domicile'] = []
            for team_obj in team_list:
                team_dict = team_obj.__dict__.copy()
                team_dict.pop('_sa_instance_state', None)
                item_dict['equipes_domicile'].append(team_dict)
            match_list = database.query(Match).filter(Match.stade_id == stadium_item.id).all()
            item_dict['matchs'] = []
            for match_obj in match_list:
                match_dict = match_obj.__dict__.copy()
                match_dict.pop('_sa_instance_state', None)
                item_dict['matchs'].append(match_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Stadium).all()


@app.get("/stadium/count/", response_model=None, tags=["Stadium"])
def get_count_stadium(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Stadium entities"""
    count = database.query(Stadium).count()
    return {"count": count}


@app.get("/stadium/paginated/", response_model=None, tags=["Stadium"])
def get_paginated_stadium(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Stadium entities"""
    total = database.query(Stadium).count()
    stadium_list = database.query(Stadium).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": stadium_list
        }

    result = []
    for stadium_item in stadium_list:
        equipes_domicile_ids = database.query(Team.id).filter(Team.stade_domicile_id == stadium_item.id).all()
        matchs_ids = database.query(Match.id).filter(Match.stade_id == stadium_item.id).all()
        item_data = {
            "stadium": stadium_item,
            "equipes_domicile_ids": [x[0] for x in equipes_domicile_ids],            "matchs_ids": [x[0] for x in matchs_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/stadium/search/", response_model=None, tags=["Stadium"])
def search_stadium(
    database: Session = Depends(get_db)
) -> list:
    """Search Stadium entities by attributes"""
    query = database.query(Stadium)


    results = query.all()
    return results


@app.get("/stadium/{stadium_id}/", response_model=None, tags=["Stadium"])
async def get_stadium(stadium_id: int, database: Session = Depends(get_db)) -> Stadium:
    db_stadium = database.query(Stadium).filter(Stadium.id == stadium_id).first()
    if db_stadium is None:
        raise HTTPException(status_code=404, detail="Stadium not found")

    equipes_domicile_ids = database.query(Team.id).filter(Team.stade_domicile_id == db_stadium.id).all()
    matchs_ids = database.query(Match.id).filter(Match.stade_id == db_stadium.id).all()
    response_data = {
        "stadium": db_stadium,
        "equipes_domicile_ids": [x[0] for x in equipes_domicile_ids],        "matchs_ids": [x[0] for x in matchs_ids]}
    return response_data



@app.post("/stadium/", response_model=None, tags=["Stadium"])
async def create_stadium(stadium_data: StadiumCreate, database: Session = Depends(get_db)) -> Stadium:


    db_stadium = Stadium(
        id=stadium_data.id,        longitude=stadium_data.longitude,        pays=stadium_data.pays,        photo_url=stadium_data.photo_url,        nom=stadium_data.nom,        capacite=stadium_data.capacite,        latitude=stadium_data.latitude,        ville=stadium_data.ville,        pelouse=stadium_data.pelouse        )

    database.add(db_stadium)
    database.commit()
    database.refresh(db_stadium)

    if stadium_data.equipes_domicile:
        # Validate that all Team IDs exist
        for team_id in stadium_data.equipes_domicile:
            db_team = database.query(Team).filter(Team.id == team_id).first()
            if not db_team:
                raise HTTPException(status_code=400, detail=f"Team with id {team_id} not found")

        # Update the related entities with the new foreign key
        database.query(Team).filter(Team.id.in_(stadium_data.equipes_domicile)).update(
            {Team.stade_domicile_id: db_stadium.id}, synchronize_session=False
        )
        database.commit()
    if stadium_data.matchs:
        # Validate that all Match IDs exist
        for match_id in stadium_data.matchs:
            db_match = database.query(Match).filter(Match.id == match_id).first()
            if not db_match:
                raise HTTPException(status_code=400, detail=f"Match with id {match_id} not found")

        # Update the related entities with the new foreign key
        database.query(Match).filter(Match.id.in_(stadium_data.matchs)).update(
            {Match.stade_id: db_stadium.id}, synchronize_session=False
        )
        database.commit()



    equipes_domicile_ids = database.query(Team.id).filter(Team.stade_domicile_id == db_stadium.id).all()
    matchs_ids = database.query(Match.id).filter(Match.stade_id == db_stadium.id).all()
    response_data = {
        "stadium": db_stadium,
        "equipes_domicile_ids": [x[0] for x in equipes_domicile_ids],        "matchs_ids": [x[0] for x in matchs_ids]    }
    return response_data


@app.post("/stadium/bulk/", response_model=None, tags=["Stadium"])
async def bulk_create_stadium(items: list[StadiumCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Stadium entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_stadium = Stadium(
                id=item_data.id,                longitude=item_data.longitude,                pays=item_data.pays,                photo_url=item_data.photo_url,                nom=item_data.nom,                capacite=item_data.capacite,                latitude=item_data.latitude,                ville=item_data.ville,                pelouse=item_data.pelouse            )
            database.add(db_stadium)
            database.flush()  # Get ID without committing
            created_items.append(db_stadium.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Stadium entities"
    }


@app.delete("/stadium/bulk/", response_model=None, tags=["Stadium"])
async def bulk_delete_stadium(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Stadium entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_stadium = database.query(Stadium).filter(Stadium.id == item_id).first()
        if db_stadium:
            database.delete(db_stadium)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Stadium entities"
    }

@app.put("/stadium/{stadium_id}/", response_model=None, tags=["Stadium"])
async def update_stadium(stadium_id: int, stadium_data: StadiumCreate, database: Session = Depends(get_db)) -> Stadium:
    db_stadium = database.query(Stadium).filter(Stadium.id == stadium_id).first()
    if db_stadium is None:
        raise HTTPException(status_code=404, detail="Stadium not found")

    setattr(db_stadium, 'id', stadium_data.id)
    setattr(db_stadium, 'longitude', stadium_data.longitude)
    setattr(db_stadium, 'pays', stadium_data.pays)
    setattr(db_stadium, 'photo_url', stadium_data.photo_url)
    setattr(db_stadium, 'nom', stadium_data.nom)
    setattr(db_stadium, 'capacite', stadium_data.capacite)
    setattr(db_stadium, 'latitude', stadium_data.latitude)
    setattr(db_stadium, 'ville', stadium_data.ville)
    setattr(db_stadium, 'pelouse', stadium_data.pelouse)
    if stadium_data.equipes_domicile is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Team).filter(Team.stade_domicile_id == db_stadium.id).update(
            {Team.stade_domicile_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if stadium_data.equipes_domicile:
            # Validate that all IDs exist
            for team_id in stadium_data.equipes_domicile:
                db_team = database.query(Team).filter(Team.id == team_id).first()
                if not db_team:
                    raise HTTPException(status_code=400, detail=f"Team with id {team_id} not found")

            # Update the related entities with the new foreign key
            database.query(Team).filter(Team.id.in_(stadium_data.equipes_domicile)).update(
                {Team.stade_domicile_id: db_stadium.id}, synchronize_session=False
            )
    if stadium_data.matchs is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Match).filter(Match.stade_id == db_stadium.id).update(
            {Match.stade_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if stadium_data.matchs:
            # Validate that all IDs exist
            for match_id in stadium_data.matchs:
                db_match = database.query(Match).filter(Match.id == match_id).first()
                if not db_match:
                    raise HTTPException(status_code=400, detail=f"Match with id {match_id} not found")

            # Update the related entities with the new foreign key
            database.query(Match).filter(Match.id.in_(stadium_data.matchs)).update(
                {Match.stade_id: db_stadium.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_stadium)

    equipes_domicile_ids = database.query(Team.id).filter(Team.stade_domicile_id == db_stadium.id).all()
    matchs_ids = database.query(Match.id).filter(Match.stade_id == db_stadium.id).all()
    response_data = {
        "stadium": db_stadium,
        "equipes_domicile_ids": [x[0] for x in equipes_domicile_ids],        "matchs_ids": [x[0] for x in matchs_ids]    }
    return response_data


@app.delete("/stadium/{stadium_id}/", response_model=None, tags=["Stadium"])
async def delete_stadium(stadium_id: int, database: Session = Depends(get_db)):
    db_stadium = database.query(Stadium).filter(Stadium.id == stadium_id).first()
    if db_stadium is None:
        raise HTTPException(status_code=404, detail="Stadium not found")
    database.delete(db_stadium)
    database.commit()
    return db_stadium


@app.get("/stadium/{stadium_id}/equipes_domicile/", response_model=None, tags=["Stadium Relationships"])
async def get_equipes_domicile_of_stadium(stadium_id: int, database: Session = Depends(get_db)):
    """Get all Team entities related to this Stadium through equipes_domicile"""
    db_stadium = database.query(Stadium).filter(Stadium.id == stadium_id).first()
    if db_stadium is None:
        raise HTTPException(status_code=404, detail="Stadium not found")

    equipes_domicile_list = database.query(Team).filter(Team.stade_domicile_id == stadium_id).all()

    return {
        "stadium_id": stadium_id,
        "equipes_domicile_count": len(equipes_domicile_list),
        "equipes_domicile": equipes_domicile_list
    }

@app.get("/stadium/{stadium_id}/matchs/", response_model=None, tags=["Stadium Relationships"])
async def get_matchs_of_stadium(stadium_id: int, database: Session = Depends(get_db)):
    """Get all Match entities related to this Stadium through matchs"""
    db_stadium = database.query(Stadium).filter(Stadium.id == stadium_id).first()
    if db_stadium is None:
        raise HTTPException(status_code=404, detail="Stadium not found")

    matchs_list = database.query(Match).filter(Match.stade_id == stadium_id).all()

    return {
        "stadium_id": stadium_id,
        "matchs_count": len(matchs_list),
        "matchs": matchs_list
    }





############################################
#
#   Notification functions
#
############################################

@app.get("/notification/", response_model=None, tags=["Notification"])
def get_all_notification(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Notification)
        query = query.options(joinedload(Notification.user))
        notification_list = query.all()

        # Serialize with relationships included
        result = []
        for notification_item in notification_list:
            item_dict = notification_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if notification_item.user:
                related_obj = notification_item.user
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['user'] = related_dict
            else:
                item_dict['user'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Notification).all()


@app.get("/notification/count/", response_model=None, tags=["Notification"])
def get_count_notification(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Notification entities"""
    count = database.query(Notification).count()
    return {"count": count}


@app.get("/notification/paginated/", response_model=None, tags=["Notification"])
def get_paginated_notification(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Notification entities"""
    total = database.query(Notification).count()
    notification_list = database.query(Notification).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": notification_list
    }


@app.get("/notification/search/", response_model=None, tags=["Notification"])
def search_notification(
    database: Session = Depends(get_db)
) -> list:
    """Search Notification entities by attributes"""
    query = database.query(Notification)


    results = query.all()
    return results


@app.get("/notification/{notification_id}/", response_model=None, tags=["Notification"])
async def get_notification(notification_id: int, database: Session = Depends(get_db)) -> Notification:
    db_notification = database.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    response_data = {
        "notification": db_notification,
}
    return response_data



@app.post("/notification/", response_model=None, tags=["Notification"])
async def create_notification(notification_data: NotificationCreate, database: Session = Depends(get_db)) -> Notification:

    if notification_data.user is not None:
        db_user = database.query(User).filter(User.id == notification_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")

    db_notification = Notification(
        created_at=notification_data.created_at,        titre=notification_data.titre,        type=notification_data.type.value,        id=notification_data.id,        contenu=notification_data.contenu,        is_read=notification_data.is_read,        user_id=notification_data.user        )

    database.add(db_notification)
    database.commit()
    database.refresh(db_notification)




    return db_notification


@app.post("/notification/bulk/", response_model=None, tags=["Notification"])
async def bulk_create_notification(items: list[NotificationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Notification entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.user:
                raise ValueError("User ID is required")

            db_notification = Notification(
                created_at=item_data.created_at,                titre=item_data.titre,                type=item_data.type.value,                id=item_data.id,                contenu=item_data.contenu,                is_read=item_data.is_read,                user_id=item_data.user            )
            database.add(db_notification)
            database.flush()  # Get ID without committing
            created_items.append(db_notification.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Notification entities"
    }


@app.delete("/notification/bulk/", response_model=None, tags=["Notification"])
async def bulk_delete_notification(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Notification entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_notification = database.query(Notification).filter(Notification.id == item_id).first()
        if db_notification:
            database.delete(db_notification)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Notification entities"
    }

@app.put("/notification/{notification_id}/", response_model=None, tags=["Notification"])
async def update_notification(notification_id: int, notification_data: NotificationCreate, database: Session = Depends(get_db)) -> Notification:
    db_notification = database.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    setattr(db_notification, 'created_at', notification_data.created_at)
    setattr(db_notification, 'titre', notification_data.titre)
    setattr(db_notification, 'type', notification_data.type.value)
    setattr(db_notification, 'id', notification_data.id)
    setattr(db_notification, 'contenu', notification_data.contenu)
    setattr(db_notification, 'is_read', notification_data.is_read)
    if notification_data.user is not None:
        db_user = database.query(User).filter(User.id == notification_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_notification, 'user_id', notification_data.user)
    database.commit()
    database.refresh(db_notification)

    return db_notification


@app.delete("/notification/{notification_id}/", response_model=None, tags=["Notification"])
async def delete_notification(notification_id: int, database: Session = Depends(get_db)):
    db_notification = database.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    database.delete(db_notification)
    database.commit()
    return db_notification






############################################
#
#   MediaFile functions
#
############################################

@app.get("/mediafile/", response_model=None, tags=["MediaFile"])
def get_all_mediafile(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(MediaFile)
        query = query.options(joinedload(MediaFile.uploader))
        mediafile_list = query.all()

        # Serialize with relationships included
        result = []
        for mediafile_item in mediafile_list:
            item_dict = mediafile_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if mediafile_item.uploader:
                related_obj = mediafile_item.uploader
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['uploader'] = related_dict
            else:
                item_dict['uploader'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(MediaFile).all()


@app.get("/mediafile/count/", response_model=None, tags=["MediaFile"])
def get_count_mediafile(database: Session = Depends(get_db)) -> dict:
    """Get the total count of MediaFile entities"""
    count = database.query(MediaFile).count()
    return {"count": count}


@app.get("/mediafile/paginated/", response_model=None, tags=["MediaFile"])
def get_paginated_mediafile(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of MediaFile entities"""
    total = database.query(MediaFile).count()
    mediafile_list = database.query(MediaFile).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": mediafile_list
    }


@app.get("/mediafile/search/", response_model=None, tags=["MediaFile"])
def search_mediafile(
    database: Session = Depends(get_db)
) -> list:
    """Search MediaFile entities by attributes"""
    query = database.query(MediaFile)


    results = query.all()
    return results


@app.get("/mediafile/{mediafile_id}/", response_model=None, tags=["MediaFile"])
async def get_mediafile(mediafile_id: int, database: Session = Depends(get_db)) -> MediaFile:
    db_mediafile = database.query(MediaFile).filter(MediaFile.id == mediafile_id).first()
    if db_mediafile is None:
        raise HTTPException(status_code=404, detail="MediaFile not found")

    response_data = {
        "mediafile": db_mediafile,
}
    return response_data



@app.post("/mediafile/", response_model=None, tags=["MediaFile"])
async def create_mediafile(mediafile_data: MediaFileCreate, database: Session = Depends(get_db)) -> MediaFile:

    if mediafile_data.uploader :
        db_uploader = database.query(User).filter(User.id == mediafile_data.uploader).first()
        if not db_uploader:
            raise HTTPException(status_code=400, detail="User not found")

    db_mediafile = MediaFile(
        id=mediafile_data.id,        alt_text=mediafile_data.alt_text,        uploaded_by=mediafile_data.uploaded_by,        mimetype=mediafile_data.mimetype,        url=mediafile_data.url,        cible_type=mediafile_data.cible_type,        created_at=mediafile_data.created_at,        cible_id=mediafile_data.cible_id,        taille_ko=mediafile_data.taille_ko,        filename=mediafile_data.filename,        uploader_id=mediafile_data.uploader        )

    database.add(db_mediafile)
    database.commit()
    database.refresh(db_mediafile)




    return db_mediafile


@app.post("/mediafile/bulk/", response_model=None, tags=["MediaFile"])
async def bulk_create_mediafile(items: list[MediaFileCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple MediaFile entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_mediafile = MediaFile(
                id=item_data.id,                alt_text=item_data.alt_text,                uploaded_by=item_data.uploaded_by,                mimetype=item_data.mimetype,                url=item_data.url,                cible_type=item_data.cible_type,                created_at=item_data.created_at,                cible_id=item_data.cible_id,                taille_ko=item_data.taille_ko,                filename=item_data.filename,                uploader_id=item_data.uploader            )
            database.add(db_mediafile)
            database.flush()  # Get ID without committing
            created_items.append(db_mediafile.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} MediaFile entities"
    }


@app.delete("/mediafile/bulk/", response_model=None, tags=["MediaFile"])
async def bulk_delete_mediafile(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple MediaFile entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_mediafile = database.query(MediaFile).filter(MediaFile.id == item_id).first()
        if db_mediafile:
            database.delete(db_mediafile)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} MediaFile entities"
    }

@app.put("/mediafile/{mediafile_id}/", response_model=None, tags=["MediaFile"])
async def update_mediafile(mediafile_id: int, mediafile_data: MediaFileCreate, database: Session = Depends(get_db)) -> MediaFile:
    db_mediafile = database.query(MediaFile).filter(MediaFile.id == mediafile_id).first()
    if db_mediafile is None:
        raise HTTPException(status_code=404, detail="MediaFile not found")

    setattr(db_mediafile, 'id', mediafile_data.id)
    setattr(db_mediafile, 'alt_text', mediafile_data.alt_text)
    setattr(db_mediafile, 'uploaded_by', mediafile_data.uploaded_by)
    setattr(db_mediafile, 'mimetype', mediafile_data.mimetype)
    setattr(db_mediafile, 'url', mediafile_data.url)
    setattr(db_mediafile, 'cible_type', mediafile_data.cible_type)
    setattr(db_mediafile, 'created_at', mediafile_data.created_at)
    setattr(db_mediafile, 'cible_id', mediafile_data.cible_id)
    setattr(db_mediafile, 'taille_ko', mediafile_data.taille_ko)
    setattr(db_mediafile, 'filename', mediafile_data.filename)
    if mediafile_data.uploader is not None:
        db_uploader = database.query(User).filter(User.id == mediafile_data.uploader).first()
        if not db_uploader:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_mediafile, 'uploader_id', mediafile_data.uploader)
    else:
        setattr(db_mediafile, 'uploader_id', None)
    database.commit()
    database.refresh(db_mediafile)

    return db_mediafile


@app.delete("/mediafile/{mediafile_id}/", response_model=None, tags=["MediaFile"])
async def delete_mediafile(mediafile_id: int, database: Session = Depends(get_db)):
    db_mediafile = database.query(MediaFile).filter(MediaFile.id == mediafile_id).first()
    if db_mediafile is None:
        raise HTTPException(status_code=404, detail="MediaFile not found")
    database.delete(db_mediafile)
    database.commit()
    return db_mediafile






############################################
#
#   Message functions
#
############################################

@app.get("/message/", response_model=None, tags=["Message"])
def get_all_message(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Message)
        query = query.options(joinedload(Message.auteur))
        query = query.options(joinedload(Message.canal))
        message_list = query.all()

        # Serialize with relationships included
        result = []
        for message_item in message_list:
            item_dict = message_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if message_item.auteur:
                related_obj = message_item.auteur
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['auteur'] = related_dict
            else:
                item_dict['auteur'] = None
            if message_item.canal:
                related_obj = message_item.canal
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['canal'] = related_dict
            else:
                item_dict['canal'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            reaction_list = database.query(Reaction).filter(Reaction.message_id == message_item.id).all()
            item_dict['reactions'] = []
            for reaction_obj in reaction_list:
                reaction_dict = reaction_obj.__dict__.copy()
                reaction_dict.pop('_sa_instance_state', None)
                item_dict['reactions'].append(reaction_dict)
            message_list = database.query(Message).filter(Message.parent_id == message_item.id).all()
            item_dict['reponses'] = []
            for message_obj in message_list:
                message_dict = message_obj.__dict__.copy()
                message_dict.pop('_sa_instance_state', None)
                item_dict['reponses'].append(message_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Message).all()


@app.get("/message/count/", response_model=None, tags=["Message"])
def get_count_message(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Message entities"""
    count = database.query(Message).count()
    return {"count": count}


@app.get("/message/paginated/", response_model=None, tags=["Message"])
def get_paginated_message(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Message entities"""
    total = database.query(Message).count()
    message_list = database.query(Message).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": message_list
        }

    result = []
    for message_item in message_list:
        reactions_ids = database.query(Reaction.id).filter(Reaction.message_id == message_item.id).all()
        reponses_ids = database.query(Message.id).filter(Message.parent_id == message_item.id).all()
        item_data = {
            "message": message_item,
            "reactions_ids": [x[0] for x in reactions_ids],            "reponses_ids": [x[0] for x in reponses_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/message/search/", response_model=None, tags=["Message"])
def search_message(
    database: Session = Depends(get_db)
) -> list:
    """Search Message entities by attributes"""
    query = database.query(Message)


    results = query.all()
    return results


@app.get("/message/{message_id}/", response_model=None, tags=["Message"])
async def get_message(message_id: int, database: Session = Depends(get_db)) -> Message:
    db_message = database.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    reactions_ids = database.query(Reaction.id).filter(Reaction.message_id == db_message.id).all()
    reponses_ids = database.query(Message.id).filter(Message.parent_id == db_message.id).all()
    response_data = {
        "message": db_message,
        "reactions_ids": [x[0] for x in reactions_ids],        "reponses_ids": [x[0] for x in reponses_ids]}
    return response_data



@app.post("/message/", response_model=None, tags=["Message"])
async def create_message(message_data: MessageCreate, database: Session = Depends(get_db)) -> Message:

    if message_data.auteur is not None:
        db_auteur = database.query(User).filter(User.id == message_data.auteur).first()
        if not db_auteur:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if message_data.canal is not None:
        db_canal = database.query(Channel).filter(Channel.id == message_data.canal).first()
        if not db_canal:
            raise HTTPException(status_code=400, detail="Channel not found")
    else:
        raise HTTPException(status_code=400, detail="Channel ID is required")

    db_message = Message(
        edited_at=message_data.edited_at,        minute_match=message_data.minute_match,        content=message_data.content,        id=message_data.id,        created_at=message_data.created_at,        is_deleted=message_data.is_deleted,        auteur_id=message_data.auteur,        canal_id=message_data.canal        )

    database.add(db_message)
    database.commit()
    database.refresh(db_message)

    if message_data.reactions:
        # Validate that all Reaction IDs exist
        for reaction_id in message_data.reactions:
            db_reaction = database.query(Reaction).filter(Reaction.id == reaction_id).first()
            if not db_reaction:
                raise HTTPException(status_code=400, detail=f"Reaction with id {reaction_id} not found")

        # Update the related entities with the new foreign key
        database.query(Reaction).filter(Reaction.id.in_(message_data.reactions)).update(
            {Reaction.message_id: db_message.id}, synchronize_session=False
        )
        database.commit()
    if message_data.reponses:
        # Validate that all Message IDs exist
        for message_id in message_data.reponses:
            db_message = database.query(Message).filter(Message.id == message_id).first()
            if not db_message:
                raise HTTPException(status_code=400, detail=f"Message with id {message_id} not found")

        # Update the related entities with the new foreign key
        database.query(Message).filter(Message.id.in_(message_data.reponses)).update(
            {Message.parent_id: db_message.id}, synchronize_session=False
        )
        database.commit()



    reactions_ids = database.query(Reaction.id).filter(Reaction.message_id == db_message.id).all()
    reponses_ids = database.query(Message.id).filter(Message.parent_id == db_message.id).all()
    response_data = {
        "message": db_message,
        "reactions_ids": [x[0] for x in reactions_ids],        "reponses_ids": [x[0] for x in reponses_ids]    }
    return response_data


@app.post("/message/bulk/", response_model=None, tags=["Message"])
async def bulk_create_message(items: list[MessageCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Message entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.auteur:
                raise ValueError("User ID is required")
            if not item_data.canal:
                raise ValueError("Channel ID is required")

            db_message = Message(
                edited_at=item_data.edited_at,                minute_match=item_data.minute_match,                content=item_data.content,                id=item_data.id,                created_at=item_data.created_at,                is_deleted=item_data.is_deleted,                auteur_id=item_data.auteur,                canal_id=item_data.canal            )
            database.add(db_message)
            database.flush()  # Get ID without committing
            created_items.append(db_message.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Message entities"
    }


@app.delete("/message/bulk/", response_model=None, tags=["Message"])
async def bulk_delete_message(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Message entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_message = database.query(Message).filter(Message.id == item_id).first()
        if db_message:
            database.delete(db_message)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Message entities"
    }

@app.put("/message/{message_id}/", response_model=None, tags=["Message"])
async def update_message(message_id: int, message_data: MessageCreate, database: Session = Depends(get_db)) -> Message:
    db_message = database.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    setattr(db_message, 'edited_at', message_data.edited_at)
    setattr(db_message, 'minute_match', message_data.minute_match)
    setattr(db_message, 'content', message_data.content)
    setattr(db_message, 'id', message_data.id)
    setattr(db_message, 'created_at', message_data.created_at)
    setattr(db_message, 'is_deleted', message_data.is_deleted)
    if message_data.auteur is not None:
        db_auteur = database.query(User).filter(User.id == message_data.auteur).first()
        if not db_auteur:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_message, 'auteur_id', message_data.auteur)
    if message_data.canal is not None:
        db_canal = database.query(Channel).filter(Channel.id == message_data.canal).first()
        if not db_canal:
            raise HTTPException(status_code=400, detail="Channel not found")
        setattr(db_message, 'canal_id', message_data.canal)
    if message_data.reactions is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Reaction).filter(Reaction.message_id == db_message.id).update(
            {Reaction.message_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if message_data.reactions:
            # Validate that all IDs exist
            for reaction_id in message_data.reactions:
                db_reaction = database.query(Reaction).filter(Reaction.id == reaction_id).first()
                if not db_reaction:
                    raise HTTPException(status_code=400, detail=f"Reaction with id {reaction_id} not found")

            # Update the related entities with the new foreign key
            database.query(Reaction).filter(Reaction.id.in_(message_data.reactions)).update(
                {Reaction.message_id: db_message.id}, synchronize_session=False
            )
    if message_data.reponses is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Message).filter(Message.parent_id == db_message.id).update(
            {Message.parent_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if message_data.reponses:
            # Validate that all IDs exist
            for message_id in message_data.reponses:
                db_message = database.query(Message).filter(Message.id == message_id).first()
                if not db_message:
                    raise HTTPException(status_code=400, detail=f"Message with id {message_id} not found")

            # Update the related entities with the new foreign key
            database.query(Message).filter(Message.id.in_(message_data.reponses)).update(
                {Message.parent_id: db_message.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_message)

    reactions_ids = database.query(Reaction.id).filter(Reaction.message_id == db_message.id).all()
    reponses_ids = database.query(Message.id).filter(Message.parent_id == db_message.id).all()
    response_data = {
        "message": db_message,
        "reactions_ids": [x[0] for x in reactions_ids],        "reponses_ids": [x[0] for x in reponses_ids]    }
    return response_data


@app.delete("/message/{message_id}/", response_model=None, tags=["Message"])
async def delete_message(message_id: int, database: Session = Depends(get_db)):
    db_message = database.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    database.delete(db_message)
    database.commit()
    return db_message


@app.get("/message/{message_id}/reactions/", response_model=None, tags=["Message Relationships"])
async def get_reactions_of_message(message_id: int, database: Session = Depends(get_db)):
    """Get all Reaction entities related to this Message through reactions"""
    db_message = database.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    reactions_list = database.query(Reaction).filter(Reaction.message_id == message_id).all()

    return {
        "message_id": message_id,
        "reactions_count": len(reactions_list),
        "reactions": reactions_list
    }

@app.get("/message/{message_id}/reponses/", response_model=None, tags=["Message Relationships"])
async def get_reponses_of_message(message_id: int, database: Session = Depends(get_db)):
    """Get all Message entities related to this Message through reponses"""
    db_message = database.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    reponses_list = database.query(Message).filter(Message.parent_id == message_id).all()

    return {
        "message_id": message_id,
        "reponses_count": len(reponses_list),
        "reponses": reponses_list
    }





############################################
#
#   BracketSlot functions
#
############################################

@app.get("/bracketslot/", response_model=None, tags=["BracketSlot"])
def get_all_bracketslot(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(BracketSlot)
        query = query.options(joinedload(BracketSlot.tour))
        query = query.options(joinedload(BracketSlot.match))
        bracketslot_list = query.all()

        # Serialize with relationships included
        result = []
        for bracketslot_item in bracketslot_list:
            item_dict = bracketslot_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if bracketslot_item.tour:
                related_obj = bracketslot_item.tour
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['tour'] = related_dict
            else:
                item_dict['tour'] = None
            if bracketslot_item.match:
                related_obj = bracketslot_item.match
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['match'] = related_dict
            else:
                item_dict['match'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(BracketSlot).all()


@app.get("/bracketslot/count/", response_model=None, tags=["BracketSlot"])
def get_count_bracketslot(database: Session = Depends(get_db)) -> dict:
    """Get the total count of BracketSlot entities"""
    count = database.query(BracketSlot).count()
    return {"count": count}


@app.get("/bracketslot/paginated/", response_model=None, tags=["BracketSlot"])
def get_paginated_bracketslot(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of BracketSlot entities"""
    total = database.query(BracketSlot).count()
    bracketslot_list = database.query(BracketSlot).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": bracketslot_list
    }


@app.get("/bracketslot/search/", response_model=None, tags=["BracketSlot"])
def search_bracketslot(
    database: Session = Depends(get_db)
) -> list:
    """Search BracketSlot entities by attributes"""
    query = database.query(BracketSlot)


    results = query.all()
    return results


@app.get("/bracketslot/{bracketslot_id}/", response_model=None, tags=["BracketSlot"])
async def get_bracketslot(bracketslot_id: int, database: Session = Depends(get_db)) -> BracketSlot:
    db_bracketslot = database.query(BracketSlot).filter(BracketSlot.id == bracketslot_id).first()
    if db_bracketslot is None:
        raise HTTPException(status_code=404, detail="BracketSlot not found")

    response_data = {
        "bracketslot": db_bracketslot,
}
    return response_data



@app.post("/bracketslot/", response_model=None, tags=["BracketSlot"])
async def create_bracketslot(bracketslot_data: BracketSlotCreate, database: Session = Depends(get_db)) -> BracketSlot:

    if bracketslot_data.tour is not None:
        db_tour = database.query(TournamentRound).filter(TournamentRound.id == bracketslot_data.tour).first()
        if not db_tour:
            raise HTTPException(status_code=400, detail="TournamentRound not found")
    else:
        raise HTTPException(status_code=400, detail="TournamentRound ID is required")
    if bracketslot_data.match is not None:
        db_match = database.query(Match).filter(Match.id == bracketslot_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
    else:
        raise HTTPException(status_code=400, detail="Match ID is required")

    db_bracketslot = BracketSlot(
        equipe_exterieur_id=bracketslot_data.equipe_exterieur_id,        position=bracketslot_data.position,        vainqueur_id=bracketslot_data.vainqueur_id,        equipe_domicile_id=bracketslot_data.equipe_domicile_id,        est_qualifie=bracketslot_data.est_qualifie,        id=bracketslot_data.id,        tour_id=bracketslot_data.tour,        match_id=bracketslot_data.match        )

    database.add(db_bracketslot)
    database.commit()
    database.refresh(db_bracketslot)




    return db_bracketslot


@app.post("/bracketslot/bulk/", response_model=None, tags=["BracketSlot"])
async def bulk_create_bracketslot(items: list[BracketSlotCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple BracketSlot entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.tour:
                raise ValueError("TournamentRound ID is required")
            if not item_data.match:
                raise ValueError("Match ID is required")

            db_bracketslot = BracketSlot(
                equipe_exterieur_id=item_data.equipe_exterieur_id,                position=item_data.position,                vainqueur_id=item_data.vainqueur_id,                equipe_domicile_id=item_data.equipe_domicile_id,                est_qualifie=item_data.est_qualifie,                id=item_data.id,                tour_id=item_data.tour,                match_id=item_data.match            )
            database.add(db_bracketslot)
            database.flush()  # Get ID without committing
            created_items.append(db_bracketslot.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} BracketSlot entities"
    }


@app.delete("/bracketslot/bulk/", response_model=None, tags=["BracketSlot"])
async def bulk_delete_bracketslot(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple BracketSlot entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_bracketslot = database.query(BracketSlot).filter(BracketSlot.id == item_id).first()
        if db_bracketslot:
            database.delete(db_bracketslot)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} BracketSlot entities"
    }

@app.put("/bracketslot/{bracketslot_id}/", response_model=None, tags=["BracketSlot"])
async def update_bracketslot(bracketslot_id: int, bracketslot_data: BracketSlotCreate, database: Session = Depends(get_db)) -> BracketSlot:
    db_bracketslot = database.query(BracketSlot).filter(BracketSlot.id == bracketslot_id).first()
    if db_bracketslot is None:
        raise HTTPException(status_code=404, detail="BracketSlot not found")

    setattr(db_bracketslot, 'equipe_exterieur_id', bracketslot_data.equipe_exterieur_id)
    setattr(db_bracketslot, 'position', bracketslot_data.position)
    setattr(db_bracketslot, 'vainqueur_id', bracketslot_data.vainqueur_id)
    setattr(db_bracketslot, 'equipe_domicile_id', bracketslot_data.equipe_domicile_id)
    setattr(db_bracketslot, 'est_qualifie', bracketslot_data.est_qualifie)
    setattr(db_bracketslot, 'id', bracketslot_data.id)
    if bracketslot_data.tour is not None:
        db_tour = database.query(TournamentRound).filter(TournamentRound.id == bracketslot_data.tour).first()
        if not db_tour:
            raise HTTPException(status_code=400, detail="TournamentRound not found")
        setattr(db_bracketslot, 'tour_id', bracketslot_data.tour)
    if bracketslot_data.match is not None:
        db_match = database.query(Match).filter(Match.id == bracketslot_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
        setattr(db_bracketslot, 'match_id', bracketslot_data.match)
    database.commit()
    database.refresh(db_bracketslot)

    return db_bracketslot


@app.delete("/bracketslot/{bracketslot_id}/", response_model=None, tags=["BracketSlot"])
async def delete_bracketslot(bracketslot_id: int, database: Session = Depends(get_db)):
    db_bracketslot = database.query(BracketSlot).filter(BracketSlot.id == bracketslot_id).first()
    if db_bracketslot is None:
        raise HTTPException(status_code=404, detail="BracketSlot not found")
    database.delete(db_bracketslot)
    database.commit()
    return db_bracketslot






############################################
#
#   MatchEvent functions
#
############################################

@app.get("/matchevent/", response_model=None, tags=["MatchEvent"])
def get_all_matchevent(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(MatchEvent)
        query = query.options(joinedload(MatchEvent.equipe))
        query = query.options(joinedload(MatchEvent.joueur))
        query = query.options(joinedload(MatchEvent.match))
        matchevent_list = query.all()

        # Serialize with relationships included
        result = []
        for matchevent_item in matchevent_list:
            item_dict = matchevent_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if matchevent_item.equipe:
                related_obj = matchevent_item.equipe
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['equipe'] = related_dict
            else:
                item_dict['equipe'] = None
            if matchevent_item.joueur:
                related_obj = matchevent_item.joueur
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['joueur'] = related_dict
            else:
                item_dict['joueur'] = None
            if matchevent_item.match:
                related_obj = matchevent_item.match
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['match'] = related_dict
            else:
                item_dict['match'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(MatchEvent).all()


@app.get("/matchevent/count/", response_model=None, tags=["MatchEvent"])
def get_count_matchevent(database: Session = Depends(get_db)) -> dict:
    """Get the total count of MatchEvent entities"""
    count = database.query(MatchEvent).count()
    return {"count": count}


@app.get("/matchevent/paginated/", response_model=None, tags=["MatchEvent"])
def get_paginated_matchevent(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of MatchEvent entities"""
    total = database.query(MatchEvent).count()
    matchevent_list = database.query(MatchEvent).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": matchevent_list
    }


@app.get("/matchevent/search/", response_model=None, tags=["MatchEvent"])
def search_matchevent(
    database: Session = Depends(get_db)
) -> list:
    """Search MatchEvent entities by attributes"""
    query = database.query(MatchEvent)


    results = query.all()
    return results


@app.get("/matchevent/{matchevent_id}/", response_model=None, tags=["MatchEvent"])
async def get_matchevent(matchevent_id: int, database: Session = Depends(get_db)) -> MatchEvent:
    db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
    if db_matchevent is None:
        raise HTTPException(status_code=404, detail="MatchEvent not found")

    response_data = {
        "matchevent": db_matchevent,
}
    return response_data



@app.post("/matchevent/", response_model=None, tags=["MatchEvent"])
async def create_matchevent(matchevent_data: MatchEventCreate, database: Session = Depends(get_db)) -> MatchEvent:

    if matchevent_data.equipe :
        db_equipe = database.query(Team).filter(Team.id == matchevent_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
    if matchevent_data.joueur :
        db_joueur = database.query(Player).filter(Player.id == matchevent_data.joueur).first()
        if not db_joueur:
            raise HTTPException(status_code=400, detail="Player not found")
    if matchevent_data.match is not None:
        db_match = database.query(Match).filter(Match.id == matchevent_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
    else:
        raise HTTPException(status_code=400, detail="Match ID is required")

    db_matchevent = MatchEvent(
        type=matchevent_data.type.value,        description=matchevent_data.description,        id=matchevent_data.id,        created_at=matchevent_data.created_at,        minute=matchevent_data.minute,        equipe_id=matchevent_data.equipe,        joueur_id=matchevent_data.joueur,        match_id=matchevent_data.match        )

    database.add(db_matchevent)
    database.commit()
    database.refresh(db_matchevent)




    return db_matchevent


@app.post("/matchevent/bulk/", response_model=None, tags=["MatchEvent"])
async def bulk_create_matchevent(items: list[MatchEventCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple MatchEvent entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.match:
                raise ValueError("Match ID is required")

            db_matchevent = MatchEvent(
                type=item_data.type.value,                description=item_data.description,                id=item_data.id,                created_at=item_data.created_at,                minute=item_data.minute,                equipe_id=item_data.equipe,                joueur_id=item_data.joueur,                match_id=item_data.match            )
            database.add(db_matchevent)
            database.flush()  # Get ID without committing
            created_items.append(db_matchevent.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} MatchEvent entities"
    }


@app.delete("/matchevent/bulk/", response_model=None, tags=["MatchEvent"])
async def bulk_delete_matchevent(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple MatchEvent entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == item_id).first()
        if db_matchevent:
            database.delete(db_matchevent)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} MatchEvent entities"
    }

@app.put("/matchevent/{matchevent_id}/", response_model=None, tags=["MatchEvent"])
async def update_matchevent(matchevent_id: int, matchevent_data: MatchEventCreate, database: Session = Depends(get_db)) -> MatchEvent:
    db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
    if db_matchevent is None:
        raise HTTPException(status_code=404, detail="MatchEvent not found")

    setattr(db_matchevent, 'type', matchevent_data.type.value)
    setattr(db_matchevent, 'description', matchevent_data.description)
    setattr(db_matchevent, 'id', matchevent_data.id)
    setattr(db_matchevent, 'created_at', matchevent_data.created_at)
    setattr(db_matchevent, 'minute', matchevent_data.minute)
    if matchevent_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == matchevent_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
        setattr(db_matchevent, 'equipe_id', matchevent_data.equipe)
    else:
        setattr(db_matchevent, 'equipe_id', None)
    if matchevent_data.joueur is not None:
        db_joueur = database.query(Player).filter(Player.id == matchevent_data.joueur).first()
        if not db_joueur:
            raise HTTPException(status_code=400, detail="Player not found")
        setattr(db_matchevent, 'joueur_id', matchevent_data.joueur)
    else:
        setattr(db_matchevent, 'joueur_id', None)
    if matchevent_data.match is not None:
        db_match = database.query(Match).filter(Match.id == matchevent_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
        setattr(db_matchevent, 'match_id', matchevent_data.match)
    database.commit()
    database.refresh(db_matchevent)

    return db_matchevent


@app.delete("/matchevent/{matchevent_id}/", response_model=None, tags=["MatchEvent"])
async def delete_matchevent(matchevent_id: int, database: Session = Depends(get_db)):
    db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
    if db_matchevent is None:
        raise HTTPException(status_code=404, detail="MatchEvent not found")
    database.delete(db_matchevent)
    database.commit()
    return db_matchevent






############################################
#
#   TournamentRound functions
#
############################################

@app.get("/tournamentround/", response_model=None, tags=["TournamentRound"])
def get_all_tournamentround(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(TournamentRound)
        query = query.options(joinedload(TournamentRound.competition))
        tournamentround_list = query.all()

        # Serialize with relationships included
        result = []
        for tournamentround_item in tournamentround_list:
            item_dict = tournamentround_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if tournamentround_item.competition:
                related_obj = tournamentround_item.competition
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['competition'] = related_dict
            else:
                item_dict['competition'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            bracketslot_list = database.query(BracketSlot).filter(BracketSlot.tour_id == tournamentround_item.id).all()
            item_dict['slots'] = []
            for bracketslot_obj in bracketslot_list:
                bracketslot_dict = bracketslot_obj.__dict__.copy()
                bracketslot_dict.pop('_sa_instance_state', None)
                item_dict['slots'].append(bracketslot_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(TournamentRound).all()


@app.get("/tournamentround/count/", response_model=None, tags=["TournamentRound"])
def get_count_tournamentround(database: Session = Depends(get_db)) -> dict:
    """Get the total count of TournamentRound entities"""
    count = database.query(TournamentRound).count()
    return {"count": count}


@app.get("/tournamentround/paginated/", response_model=None, tags=["TournamentRound"])
def get_paginated_tournamentround(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of TournamentRound entities"""
    total = database.query(TournamentRound).count()
    tournamentround_list = database.query(TournamentRound).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": tournamentround_list
        }

    result = []
    for tournamentround_item in tournamentround_list:
        slots_ids = database.query(BracketSlot.id).filter(BracketSlot.tour_id == tournamentround_item.id).all()
        item_data = {
            "tournamentround": tournamentround_item,
            "slots_ids": [x[0] for x in slots_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/tournamentround/search/", response_model=None, tags=["TournamentRound"])
def search_tournamentround(
    database: Session = Depends(get_db)
) -> list:
    """Search TournamentRound entities by attributes"""
    query = database.query(TournamentRound)


    results = query.all()
    return results


@app.get("/tournamentround/{tournamentround_id}/", response_model=None, tags=["TournamentRound"])
async def get_tournamentround(tournamentround_id: int, database: Session = Depends(get_db)) -> TournamentRound:
    db_tournamentround = database.query(TournamentRound).filter(TournamentRound.id == tournamentround_id).first()
    if db_tournamentround is None:
        raise HTTPException(status_code=404, detail="TournamentRound not found")

    slots_ids = database.query(BracketSlot.id).filter(BracketSlot.tour_id == db_tournamentround.id).all()
    response_data = {
        "tournamentround": db_tournamentround,
        "slots_ids": [x[0] for x in slots_ids]}
    return response_data



@app.post("/tournamentround/", response_model=None, tags=["TournamentRound"])
async def create_tournamentround(tournamentround_data: TournamentRoundCreate, database: Session = Depends(get_db)) -> TournamentRound:

    if tournamentround_data.competition is not None:
        db_competition = database.query(Competition).filter(Competition.id == tournamentround_data.competition).first()
        if not db_competition:
            raise HTTPException(status_code=400, detail="Competition not found")
    else:
        raise HTTPException(status_code=400, detail="Competition ID is required")

    db_tournamentround = TournamentRound(
        date_debut=tournamentround_data.date_debut,        nom=tournamentround_data.nom,        date_fin=tournamentround_data.date_fin,        statut=tournamentround_data.statut.value,        numero=tournamentround_data.numero,        id=tournamentround_data.id,        competition_id=tournamentround_data.competition        )

    database.add(db_tournamentround)
    database.commit()
    database.refresh(db_tournamentround)

    if tournamentround_data.slots:
        # Validate that all BracketSlot IDs exist
        for bracketslot_id in tournamentround_data.slots:
            db_bracketslot = database.query(BracketSlot).filter(BracketSlot.id == bracketslot_id).first()
            if not db_bracketslot:
                raise HTTPException(status_code=400, detail=f"BracketSlot with id {bracketslot_id} not found")

        # Update the related entities with the new foreign key
        database.query(BracketSlot).filter(BracketSlot.id.in_(tournamentround_data.slots)).update(
            {BracketSlot.tour_id: db_tournamentround.id}, synchronize_session=False
        )
        database.commit()



    slots_ids = database.query(BracketSlot.id).filter(BracketSlot.tour_id == db_tournamentround.id).all()
    response_data = {
        "tournamentround": db_tournamentround,
        "slots_ids": [x[0] for x in slots_ids]    }
    return response_data


@app.post("/tournamentround/bulk/", response_model=None, tags=["TournamentRound"])
async def bulk_create_tournamentround(items: list[TournamentRoundCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple TournamentRound entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.competition:
                raise ValueError("Competition ID is required")

            db_tournamentround = TournamentRound(
                date_debut=item_data.date_debut,                nom=item_data.nom,                date_fin=item_data.date_fin,                statut=item_data.statut.value,                numero=item_data.numero,                id=item_data.id,                competition_id=item_data.competition            )
            database.add(db_tournamentround)
            database.flush()  # Get ID without committing
            created_items.append(db_tournamentround.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} TournamentRound entities"
    }


@app.delete("/tournamentround/bulk/", response_model=None, tags=["TournamentRound"])
async def bulk_delete_tournamentround(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple TournamentRound entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_tournamentround = database.query(TournamentRound).filter(TournamentRound.id == item_id).first()
        if db_tournamentround:
            database.delete(db_tournamentround)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} TournamentRound entities"
    }

@app.put("/tournamentround/{tournamentround_id}/", response_model=None, tags=["TournamentRound"])
async def update_tournamentround(tournamentround_id: int, tournamentround_data: TournamentRoundCreate, database: Session = Depends(get_db)) -> TournamentRound:
    db_tournamentround = database.query(TournamentRound).filter(TournamentRound.id == tournamentround_id).first()
    if db_tournamentround is None:
        raise HTTPException(status_code=404, detail="TournamentRound not found")

    setattr(db_tournamentround, 'date_debut', tournamentround_data.date_debut)
    setattr(db_tournamentround, 'nom', tournamentround_data.nom)
    setattr(db_tournamentround, 'date_fin', tournamentround_data.date_fin)
    setattr(db_tournamentround, 'statut', tournamentround_data.statut.value)
    setattr(db_tournamentround, 'numero', tournamentround_data.numero)
    setattr(db_tournamentround, 'id', tournamentround_data.id)
    if tournamentround_data.competition is not None:
        db_competition = database.query(Competition).filter(Competition.id == tournamentround_data.competition).first()
        if not db_competition:
            raise HTTPException(status_code=400, detail="Competition not found")
        setattr(db_tournamentround, 'competition_id', tournamentround_data.competition)
    if tournamentround_data.slots is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(BracketSlot).filter(BracketSlot.tour_id == db_tournamentround.id).update(
            {BracketSlot.tour_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if tournamentround_data.slots:
            # Validate that all IDs exist
            for bracketslot_id in tournamentround_data.slots:
                db_bracketslot = database.query(BracketSlot).filter(BracketSlot.id == bracketslot_id).first()
                if not db_bracketslot:
                    raise HTTPException(status_code=400, detail=f"BracketSlot with id {bracketslot_id} not found")

            # Update the related entities with the new foreign key
            database.query(BracketSlot).filter(BracketSlot.id.in_(tournamentround_data.slots)).update(
                {BracketSlot.tour_id: db_tournamentround.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_tournamentround)

    slots_ids = database.query(BracketSlot.id).filter(BracketSlot.tour_id == db_tournamentround.id).all()
    response_data = {
        "tournamentround": db_tournamentround,
        "slots_ids": [x[0] for x in slots_ids]    }
    return response_data


@app.delete("/tournamentround/{tournamentround_id}/", response_model=None, tags=["TournamentRound"])
async def delete_tournamentround(tournamentround_id: int, database: Session = Depends(get_db)):
    db_tournamentround = database.query(TournamentRound).filter(TournamentRound.id == tournamentround_id).first()
    if db_tournamentround is None:
        raise HTTPException(status_code=404, detail="TournamentRound not found")
    database.delete(db_tournamentround)
    database.commit()
    return db_tournamentround


@app.get("/tournamentround/{tournamentround_id}/slots/", response_model=None, tags=["TournamentRound Relationships"])
async def get_slots_of_tournamentround(tournamentround_id: int, database: Session = Depends(get_db)):
    """Get all BracketSlot entities related to this TournamentRound through slots"""
    db_tournamentround = database.query(TournamentRound).filter(TournamentRound.id == tournamentround_id).first()
    if db_tournamentround is None:
        raise HTTPException(status_code=404, detail="TournamentRound not found")

    slots_list = database.query(BracketSlot).filter(BracketSlot.tour_id == tournamentround_id).all()

    return {
        "tournamentround_id": tournamentround_id,
        "slots_count": len(slots_list),
        "slots": slots_list
    }





############################################
#
#   Match functions
#
############################################

@app.get("/match/", response_model=None, tags=["Match"])
def get_all_match(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Match)
        query = query.options(joinedload(Match.stade))
        query = query.options(joinedload(Match.slot))
        query = query.options(joinedload(Match.equipe_domicile))
        query = query.options(joinedload(Match.competition))
        query = query.options(joinedload(Match.equipe_exterieure))
        query = query.options(joinedload(Match.statistiques))
        query = query.options(joinedload(Match.preview))
        query = query.options(joinedload(Match.cotes))
        match_list = query.all()

        # Serialize with relationships included
        result = []
        for match_item in match_list:
            item_dict = match_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if match_item.stade:
                related_obj = match_item.stade
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['stade'] = related_dict
            else:
                item_dict['stade'] = None
            if match_item.slot:
                related_obj = match_item.slot
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['slot'] = related_dict
            else:
                item_dict['slot'] = None
            if match_item.equipe_domicile:
                related_obj = match_item.equipe_domicile
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['equipe_domicile'] = related_dict
            else:
                item_dict['equipe_domicile'] = None
            if match_item.competition:
                related_obj = match_item.competition
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['competition'] = related_dict
            else:
                item_dict['competition'] = None
            if match_item.equipe_exterieure:
                related_obj = match_item.equipe_exterieure
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['equipe_exterieure'] = related_dict
            else:
                item_dict['equipe_exterieure'] = None
            if match_item.statistiques:
                related_obj = match_item.statistiques
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['statistiques'] = related_dict
            else:
                item_dict['statistiques'] = None
            if match_item.preview:
                related_obj = match_item.preview
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['preview'] = related_dict
            else:
                item_dict['preview'] = None
            if match_item.cotes:
                related_obj = match_item.cotes
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['cotes'] = related_dict
            else:
                item_dict['cotes'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            lineup_list = database.query(Lineup).filter(Lineup.match_id == match_item.id).all()
            item_dict['compositions'] = []
            for lineup_obj in lineup_list:
                lineup_dict = lineup_obj.__dict__.copy()
                lineup_dict.pop('_sa_instance_state', None)
                item_dict['compositions'].append(lineup_dict)
            channel_list = database.query(Channel).filter(Channel.match_id == match_item.id).all()
            item_dict['canaux'] = []
            for channel_obj in channel_list:
                channel_dict = channel_obj.__dict__.copy()
                channel_dict.pop('_sa_instance_state', None)
                item_dict['canaux'].append(channel_dict)
            matchevent_list = database.query(MatchEvent).filter(MatchEvent.match_id == match_item.id).all()
            item_dict['evenements'] = []
            for matchevent_obj in matchevent_list:
                matchevent_dict = matchevent_obj.__dict__.copy()
                matchevent_dict.pop('_sa_instance_state', None)
                item_dict['evenements'].append(matchevent_dict)
            tennisset_list = database.query(TennisSet).filter(TennisSet.match_id == match_item.id).all()
            item_dict['sets'] = []
            for tennisset_obj in tennisset_list:
                tennisset_dict = tennisset_obj.__dict__.copy()
                tennisset_dict.pop('_sa_instance_state', None)
                item_dict['sets'].append(tennisset_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Match).all()


@app.get("/match/count/", response_model=None, tags=["Match"])
def get_count_match(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Match entities"""
    count = database.query(Match).count()
    return {"count": count}


@app.get("/match/paginated/", response_model=None, tags=["Match"])
def get_paginated_match(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Match entities"""
    total = database.query(Match).count()
    match_list = database.query(Match).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": match_list
        }

    result = []
    for match_item in match_list:
        compositions_ids = database.query(Lineup.id).filter(Lineup.match_id == match_item.id).all()
        canaux_ids = database.query(Channel.id).filter(Channel.match_id == match_item.id).all()
        evenements_ids = database.query(MatchEvent.id).filter(MatchEvent.match_id == match_item.id).all()
        sets_ids = database.query(TennisSet.id).filter(TennisSet.match_id == match_item.id).all()
        item_data = {
            "match": match_item,
            "compositions_ids": [x[0] for x in compositions_ids],            "canaux_ids": [x[0] for x in canaux_ids],            "evenements_ids": [x[0] for x in evenements_ids],            "sets_ids": [x[0] for x in sets_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/match/search/", response_model=None, tags=["Match"])
def search_match(
    database: Session = Depends(get_db)
) -> list:
    """Search Match entities by attributes"""
    query = database.query(Match)


    results = query.all()
    return results


@app.get("/match/{match_id}/", response_model=None, tags=["Match"])
async def get_match(match_id: int, database: Session = Depends(get_db)) -> Match:
    db_match = database.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    compositions_ids = database.query(Lineup.id).filter(Lineup.match_id == db_match.id).all()
    canaux_ids = database.query(Channel.id).filter(Channel.match_id == db_match.id).all()
    evenements_ids = database.query(MatchEvent.id).filter(MatchEvent.match_id == db_match.id).all()
    sets_ids = database.query(TennisSet.id).filter(TennisSet.match_id == db_match.id).all()
    response_data = {
        "match": db_match,
        "compositions_ids": [x[0] for x in compositions_ids],        "canaux_ids": [x[0] for x in canaux_ids],        "evenements_ids": [x[0] for x in evenements_ids],        "sets_ids": [x[0] for x in sets_ids]}
    return response_data



@app.post("/match/", response_model=None, tags=["Match"])
async def create_match(match_data: MatchCreate, database: Session = Depends(get_db)) -> Match:

    if match_data.stade :
        db_stade = database.query(Stadium).filter(Stadium.id == match_data.stade).first()
        if not db_stade:
            raise HTTPException(status_code=400, detail="Stadium not found")
    if match_data.equipe_domicile is not None:
        db_equipe_domicile = database.query(Team).filter(Team.id == match_data.equipe_domicile).first()
        if not db_equipe_domicile:
            raise HTTPException(status_code=400, detail="Team not found")
    else:
        raise HTTPException(status_code=400, detail="Team ID is required")
    if match_data.competition is not None:
        db_competition = database.query(Competition).filter(Competition.id == match_data.competition).first()
        if not db_competition:
            raise HTTPException(status_code=400, detail="Competition not found")
    else:
        raise HTTPException(status_code=400, detail="Competition ID is required")
    if match_data.equipe_exterieure is not None:
        db_equipe_exterieure = database.query(Team).filter(Team.id == match_data.equipe_exterieure).first()
        if not db_equipe_exterieure:
            raise HTTPException(status_code=400, detail="Team not found")
    else:
        raise HTTPException(status_code=400, detail="Team ID is required")

    db_match = Match(
        score_jeu_actuel=match_data.score_jeu_actuel,        type_match=match_data.type_match.value,        status=match_data.status.value,        progression=match_data.progression,        created_at=match_data.created_at,        surface=match_data.surface.value,        journee=match_data.journee,        serveur_id=match_data.serveur_id,        updated_at=match_data.updated_at,        score_domicile=match_data.score_domicile,        date_heure=match_data.date_heure,        set_actuel=match_data.set_actuel,        lieu=match_data.lieu,        tour_tournoi=match_data.tour_tournoi,        score_exterieur=match_data.score_exterieur,        id=match_data.id,        stade_id=match_data.stade,        equipe_domicile_id=match_data.equipe_domicile,        competition_id=match_data.competition,        equipe_exterieure_id=match_data.equipe_exterieure        )

    database.add(db_match)
    database.commit()
    database.refresh(db_match)

    if match_data.compositions:
        # Validate that all Lineup IDs exist
        for lineup_id in match_data.compositions:
            db_lineup = database.query(Lineup).filter(Lineup.id == lineup_id).first()
            if not db_lineup:
                raise HTTPException(status_code=400, detail=f"Lineup with id {lineup_id} not found")

        # Update the related entities with the new foreign key
        database.query(Lineup).filter(Lineup.id.in_(match_data.compositions)).update(
            {Lineup.match_id: db_match.id}, synchronize_session=False
        )
        database.commit()
    if match_data.canaux:
        # Validate that all Channel IDs exist
        for channel_id in match_data.canaux:
            db_channel = database.query(Channel).filter(Channel.id == channel_id).first()
            if not db_channel:
                raise HTTPException(status_code=400, detail=f"Channel with id {channel_id} not found")

        # Update the related entities with the new foreign key
        database.query(Channel).filter(Channel.id.in_(match_data.canaux)).update(
            {Channel.match_id: db_match.id}, synchronize_session=False
        )
        database.commit()
    if match_data.evenements:
        # Validate that all MatchEvent IDs exist
        for matchevent_id in match_data.evenements:
            db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
            if not db_matchevent:
                raise HTTPException(status_code=400, detail=f"MatchEvent with id {matchevent_id} not found")

        # Update the related entities with the new foreign key
        database.query(MatchEvent).filter(MatchEvent.id.in_(match_data.evenements)).update(
            {MatchEvent.match_id: db_match.id}, synchronize_session=False
        )
        database.commit()
    if match_data.sets:
        # Validate that all TennisSet IDs exist
        for tennisset_id in match_data.sets:
            db_tennisset = database.query(TennisSet).filter(TennisSet.id == tennisset_id).first()
            if not db_tennisset:
                raise HTTPException(status_code=400, detail=f"TennisSet with id {tennisset_id} not found")

        # Update the related entities with the new foreign key
        database.query(TennisSet).filter(TennisSet.id.in_(match_data.sets)).update(
            {TennisSet.match_id: db_match.id}, synchronize_session=False
        )
        database.commit()



    compositions_ids = database.query(Lineup.id).filter(Lineup.match_id == db_match.id).all()
    canaux_ids = database.query(Channel.id).filter(Channel.match_id == db_match.id).all()
    evenements_ids = database.query(MatchEvent.id).filter(MatchEvent.match_id == db_match.id).all()
    sets_ids = database.query(TennisSet.id).filter(TennisSet.match_id == db_match.id).all()
    response_data = {
        "match": db_match,
        "compositions_ids": [x[0] for x in compositions_ids],        "canaux_ids": [x[0] for x in canaux_ids],        "evenements_ids": [x[0] for x in evenements_ids],        "sets_ids": [x[0] for x in sets_ids]    }
    return response_data


@app.post("/match/bulk/", response_model=None, tags=["Match"])
async def bulk_create_match(items: list[MatchCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Match entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.equipe_domicile:
                raise ValueError("Team ID is required")
            if not item_data.competition:
                raise ValueError("Competition ID is required")
            if not item_data.equipe_exterieure:
                raise ValueError("Team ID is required")

            db_match = Match(
                score_jeu_actuel=item_data.score_jeu_actuel,                type_match=item_data.type_match.value,                status=item_data.status.value,                progression=item_data.progression,                created_at=item_data.created_at,                surface=item_data.surface.value,                journee=item_data.journee,                serveur_id=item_data.serveur_id,                updated_at=item_data.updated_at,                score_domicile=item_data.score_domicile,                date_heure=item_data.date_heure,                set_actuel=item_data.set_actuel,                lieu=item_data.lieu,                tour_tournoi=item_data.tour_tournoi,                score_exterieur=item_data.score_exterieur,                id=item_data.id,                stade_id=item_data.stade,                equipe_domicile_id=item_data.equipe_domicile,                competition_id=item_data.competition,                equipe_exterieure_id=item_data.equipe_exterieure            )
            database.add(db_match)
            database.flush()  # Get ID without committing
            created_items.append(db_match.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Match entities"
    }


@app.delete("/match/bulk/", response_model=None, tags=["Match"])
async def bulk_delete_match(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Match entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_match = database.query(Match).filter(Match.id == item_id).first()
        if db_match:
            database.delete(db_match)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Match entities"
    }

@app.put("/match/{match_id}/", response_model=None, tags=["Match"])
async def update_match(match_id: int, match_data: MatchCreate, database: Session = Depends(get_db)) -> Match:
    db_match = database.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    setattr(db_match, 'score_jeu_actuel', match_data.score_jeu_actuel)
    setattr(db_match, 'type_match', match_data.type_match.value)
    setattr(db_match, 'status', match_data.status.value)
    setattr(db_match, 'progression', match_data.progression)
    setattr(db_match, 'created_at', match_data.created_at)
    setattr(db_match, 'surface', match_data.surface.value)
    setattr(db_match, 'journee', match_data.journee)
    setattr(db_match, 'serveur_id', match_data.serveur_id)
    setattr(db_match, 'updated_at', match_data.updated_at)
    setattr(db_match, 'score_domicile', match_data.score_domicile)
    setattr(db_match, 'date_heure', match_data.date_heure)
    setattr(db_match, 'set_actuel', match_data.set_actuel)
    setattr(db_match, 'lieu', match_data.lieu)
    setattr(db_match, 'tour_tournoi', match_data.tour_tournoi)
    setattr(db_match, 'score_exterieur', match_data.score_exterieur)
    setattr(db_match, 'id', match_data.id)
    if match_data.stade is not None:
        db_stade = database.query(Stadium).filter(Stadium.id == match_data.stade).first()
        if not db_stade:
            raise HTTPException(status_code=400, detail="Stadium not found")
        setattr(db_match, 'stade_id', match_data.stade)
    else:
        setattr(db_match, 'stade_id', None)
    if match_data.equipe_domicile is not None:
        db_equipe_domicile = database.query(Team).filter(Team.id == match_data.equipe_domicile).first()
        if not db_equipe_domicile:
            raise HTTPException(status_code=400, detail="Team not found")
        setattr(db_match, 'equipe_domicile_id', match_data.equipe_domicile)
    if match_data.competition is not None:
        db_competition = database.query(Competition).filter(Competition.id == match_data.competition).first()
        if not db_competition:
            raise HTTPException(status_code=400, detail="Competition not found")
        setattr(db_match, 'competition_id', match_data.competition)
    if match_data.equipe_exterieure is not None:
        db_equipe_exterieure = database.query(Team).filter(Team.id == match_data.equipe_exterieure).first()
        if not db_equipe_exterieure:
            raise HTTPException(status_code=400, detail="Team not found")
        setattr(db_match, 'equipe_exterieure_id', match_data.equipe_exterieure)
    if match_data.compositions is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Lineup).filter(Lineup.match_id == db_match.id).update(
            {Lineup.match_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if match_data.compositions:
            # Validate that all IDs exist
            for lineup_id in match_data.compositions:
                db_lineup = database.query(Lineup).filter(Lineup.id == lineup_id).first()
                if not db_lineup:
                    raise HTTPException(status_code=400, detail=f"Lineup with id {lineup_id} not found")

            # Update the related entities with the new foreign key
            database.query(Lineup).filter(Lineup.id.in_(match_data.compositions)).update(
                {Lineup.match_id: db_match.id}, synchronize_session=False
            )
    if match_data.canaux is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Channel).filter(Channel.match_id == db_match.id).update(
            {Channel.match_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if match_data.canaux:
            # Validate that all IDs exist
            for channel_id in match_data.canaux:
                db_channel = database.query(Channel).filter(Channel.id == channel_id).first()
                if not db_channel:
                    raise HTTPException(status_code=400, detail=f"Channel with id {channel_id} not found")

            # Update the related entities with the new foreign key
            database.query(Channel).filter(Channel.id.in_(match_data.canaux)).update(
                {Channel.match_id: db_match.id}, synchronize_session=False
            )
    if match_data.evenements is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(MatchEvent).filter(MatchEvent.match_id == db_match.id).update(
            {MatchEvent.match_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if match_data.evenements:
            # Validate that all IDs exist
            for matchevent_id in match_data.evenements:
                db_matchevent = database.query(MatchEvent).filter(MatchEvent.id == matchevent_id).first()
                if not db_matchevent:
                    raise HTTPException(status_code=400, detail=f"MatchEvent with id {matchevent_id} not found")

            # Update the related entities with the new foreign key
            database.query(MatchEvent).filter(MatchEvent.id.in_(match_data.evenements)).update(
                {MatchEvent.match_id: db_match.id}, synchronize_session=False
            )
    if match_data.sets is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(TennisSet).filter(TennisSet.match_id == db_match.id).update(
            {TennisSet.match_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if match_data.sets:
            # Validate that all IDs exist
            for tennisset_id in match_data.sets:
                db_tennisset = database.query(TennisSet).filter(TennisSet.id == tennisset_id).first()
                if not db_tennisset:
                    raise HTTPException(status_code=400, detail=f"TennisSet with id {tennisset_id} not found")

            # Update the related entities with the new foreign key
            database.query(TennisSet).filter(TennisSet.id.in_(match_data.sets)).update(
                {TennisSet.match_id: db_match.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_match)

    compositions_ids = database.query(Lineup.id).filter(Lineup.match_id == db_match.id).all()
    canaux_ids = database.query(Channel.id).filter(Channel.match_id == db_match.id).all()
    evenements_ids = database.query(MatchEvent.id).filter(MatchEvent.match_id == db_match.id).all()
    sets_ids = database.query(TennisSet.id).filter(TennisSet.match_id == db_match.id).all()
    response_data = {
        "match": db_match,
        "compositions_ids": [x[0] for x in compositions_ids],        "canaux_ids": [x[0] for x in canaux_ids],        "evenements_ids": [x[0] for x in evenements_ids],        "sets_ids": [x[0] for x in sets_ids]    }
    return response_data


@app.delete("/match/{match_id}/", response_model=None, tags=["Match"])
async def delete_match(match_id: int, database: Session = Depends(get_db)):
    db_match = database.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    database.delete(db_match)
    database.commit()
    return db_match


@app.get("/match/{match_id}/compositions/", response_model=None, tags=["Match Relationships"])
async def get_compositions_of_match(match_id: int, database: Session = Depends(get_db)):
    """Get all Lineup entities related to this Match through compositions"""
    db_match = database.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    compositions_list = database.query(Lineup).filter(Lineup.match_id == match_id).all()

    return {
        "match_id": match_id,
        "compositions_count": len(compositions_list),
        "compositions": compositions_list
    }

@app.get("/match/{match_id}/canaux/", response_model=None, tags=["Match Relationships"])
async def get_canaux_of_match(match_id: int, database: Session = Depends(get_db)):
    """Get all Channel entities related to this Match through canaux"""
    db_match = database.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    canaux_list = database.query(Channel).filter(Channel.match_id == match_id).all()

    return {
        "match_id": match_id,
        "canaux_count": len(canaux_list),
        "canaux": canaux_list
    }

@app.get("/match/{match_id}/evenements/", response_model=None, tags=["Match Relationships"])
async def get_evenements_of_match(match_id: int, database: Session = Depends(get_db)):
    """Get all MatchEvent entities related to this Match through evenements"""
    db_match = database.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    evenements_list = database.query(MatchEvent).filter(MatchEvent.match_id == match_id).all()

    return {
        "match_id": match_id,
        "evenements_count": len(evenements_list),
        "evenements": evenements_list
    }

@app.get("/match/{match_id}/sets/", response_model=None, tags=["Match Relationships"])
async def get_sets_of_match(match_id: int, database: Session = Depends(get_db)):
    """Get all TennisSet entities related to this Match through sets"""
    db_match = database.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    sets_list = database.query(TennisSet).filter(TennisSet.match_id == match_id).all()

    return {
        "match_id": match_id,
        "sets_count": len(sets_list),
        "sets": sets_list
    }





############################################
#
#   Friendship functions
#
############################################

@app.get("/friendship/", response_model=None, tags=["Friendship"])
def get_all_friendship(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Friendship)
        query = query.options(joinedload(Friendship.demandeur))
        query = query.options(joinedload(Friendship.receveur))
        friendship_list = query.all()

        # Serialize with relationships included
        result = []
        for friendship_item in friendship_list:
            item_dict = friendship_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if friendship_item.demandeur:
                related_obj = friendship_item.demandeur
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['demandeur'] = related_dict
            else:
                item_dict['demandeur'] = None
            if friendship_item.receveur:
                related_obj = friendship_item.receveur
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['receveur'] = related_dict
            else:
                item_dict['receveur'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Friendship).all()


@app.get("/friendship/count/", response_model=None, tags=["Friendship"])
def get_count_friendship(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Friendship entities"""
    count = database.query(Friendship).count()
    return {"count": count}


@app.get("/friendship/paginated/", response_model=None, tags=["Friendship"])
def get_paginated_friendship(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Friendship entities"""
    total = database.query(Friendship).count()
    friendship_list = database.query(Friendship).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": friendship_list
    }


@app.get("/friendship/search/", response_model=None, tags=["Friendship"])
def search_friendship(
    database: Session = Depends(get_db)
) -> list:
    """Search Friendship entities by attributes"""
    query = database.query(Friendship)


    results = query.all()
    return results


@app.get("/friendship/{friendship_id}/", response_model=None, tags=["Friendship"])
async def get_friendship(friendship_id: int, database: Session = Depends(get_db)) -> Friendship:
    db_friendship = database.query(Friendship).filter(Friendship.id == friendship_id).first()
    if db_friendship is None:
        raise HTTPException(status_code=404, detail="Friendship not found")

    response_data = {
        "friendship": db_friendship,
}
    return response_data



@app.post("/friendship/", response_model=None, tags=["Friendship"])
async def create_friendship(friendship_data: FriendshipCreate, database: Session = Depends(get_db)) -> Friendship:

    if friendship_data.demandeur is not None:
        db_demandeur = database.query(User).filter(User.id == friendship_data.demandeur).first()
        if not db_demandeur:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if friendship_data.receveur is not None:
        db_receveur = database.query(User).filter(User.id == friendship_data.receveur).first()
        if not db_receveur:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")

    db_friendship = Friendship(
        id=friendship_data.id,        updated_at=friendship_data.updated_at,        created_at=friendship_data.created_at,        status=friendship_data.status.value,        demandeur_id=friendship_data.demandeur,        receveur_id=friendship_data.receveur        )

    database.add(db_friendship)
    database.commit()
    database.refresh(db_friendship)




    return db_friendship


@app.post("/friendship/bulk/", response_model=None, tags=["Friendship"])
async def bulk_create_friendship(items: list[FriendshipCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Friendship entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.demandeur:
                raise ValueError("User ID is required")
            if not item_data.receveur:
                raise ValueError("User ID is required")

            db_friendship = Friendship(
                id=item_data.id,                updated_at=item_data.updated_at,                created_at=item_data.created_at,                status=item_data.status.value,                demandeur_id=item_data.demandeur,                receveur_id=item_data.receveur            )
            database.add(db_friendship)
            database.flush()  # Get ID without committing
            created_items.append(db_friendship.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Friendship entities"
    }


@app.delete("/friendship/bulk/", response_model=None, tags=["Friendship"])
async def bulk_delete_friendship(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Friendship entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_friendship = database.query(Friendship).filter(Friendship.id == item_id).first()
        if db_friendship:
            database.delete(db_friendship)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Friendship entities"
    }

@app.put("/friendship/{friendship_id}/", response_model=None, tags=["Friendship"])
async def update_friendship(friendship_id: int, friendship_data: FriendshipCreate, database: Session = Depends(get_db)) -> Friendship:
    db_friendship = database.query(Friendship).filter(Friendship.id == friendship_id).first()
    if db_friendship is None:
        raise HTTPException(status_code=404, detail="Friendship not found")

    setattr(db_friendship, 'id', friendship_data.id)
    setattr(db_friendship, 'updated_at', friendship_data.updated_at)
    setattr(db_friendship, 'created_at', friendship_data.created_at)
    setattr(db_friendship, 'status', friendship_data.status.value)
    if friendship_data.demandeur is not None:
        db_demandeur = database.query(User).filter(User.id == friendship_data.demandeur).first()
        if not db_demandeur:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_friendship, 'demandeur_id', friendship_data.demandeur)
    if friendship_data.receveur is not None:
        db_receveur = database.query(User).filter(User.id == friendship_data.receveur).first()
        if not db_receveur:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_friendship, 'receveur_id', friendship_data.receveur)
    database.commit()
    database.refresh(db_friendship)

    return db_friendship


@app.delete("/friendship/{friendship_id}/", response_model=None, tags=["Friendship"])
async def delete_friendship(friendship_id: int, database: Session = Depends(get_db)):
    db_friendship = database.query(Friendship).filter(Friendship.id == friendship_id).first()
    if db_friendship is None:
        raise HTTPException(status_code=404, detail="Friendship not found")
    database.delete(db_friendship)
    database.commit()
    return db_friendship






############################################
#
#   FavoritePlayer functions
#
############################################

@app.get("/favoriteplayer/", response_model=None, tags=["FavoritePlayer"])
def get_all_favoriteplayer(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(FavoritePlayer)
        query = query.options(joinedload(FavoritePlayer.user))
        favoriteplayer_list = query.all()

        # Serialize with relationships included
        result = []
        for favoriteplayer_item in favoriteplayer_list:
            item_dict = favoriteplayer_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if favoriteplayer_item.user:
                related_obj = favoriteplayer_item.user
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['user'] = related_dict
            else:
                item_dict['user'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            player_list = database.query(Player).filter(Player.joueur_id == favoriteplayer_item.id).all()
            item_dict['fans'] = []
            for player_obj in player_list:
                player_dict = player_obj.__dict__.copy()
                player_dict.pop('_sa_instance_state', None)
                item_dict['fans'].append(player_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(FavoritePlayer).all()


@app.get("/favoriteplayer/count/", response_model=None, tags=["FavoritePlayer"])
def get_count_favoriteplayer(database: Session = Depends(get_db)) -> dict:
    """Get the total count of FavoritePlayer entities"""
    count = database.query(FavoritePlayer).count()
    return {"count": count}


@app.get("/favoriteplayer/paginated/", response_model=None, tags=["FavoritePlayer"])
def get_paginated_favoriteplayer(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of FavoritePlayer entities"""
    total = database.query(FavoritePlayer).count()
    favoriteplayer_list = database.query(FavoritePlayer).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": favoriteplayer_list
        }

    result = []
    for favoriteplayer_item in favoriteplayer_list:
        fans_ids = database.query(Player.id).filter(Player.joueur_id == favoriteplayer_item.id).all()
        item_data = {
            "favoriteplayer": favoriteplayer_item,
            "fans_ids": [x[0] for x in fans_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/favoriteplayer/search/", response_model=None, tags=["FavoritePlayer"])
def search_favoriteplayer(
    database: Session = Depends(get_db)
) -> list:
    """Search FavoritePlayer entities by attributes"""
    query = database.query(FavoritePlayer)


    results = query.all()
    return results


@app.get("/favoriteplayer/{favoriteplayer_id}/", response_model=None, tags=["FavoritePlayer"])
async def get_favoriteplayer(favoriteplayer_id: int, database: Session = Depends(get_db)) -> FavoritePlayer:
    db_favoriteplayer = database.query(FavoritePlayer).filter(FavoritePlayer.id == favoriteplayer_id).first()
    if db_favoriteplayer is None:
        raise HTTPException(status_code=404, detail="FavoritePlayer not found")

    fans_ids = database.query(Player.id).filter(Player.joueur_id == db_favoriteplayer.id).all()
    response_data = {
        "favoriteplayer": db_favoriteplayer,
        "fans_ids": [x[0] for x in fans_ids]}
    return response_data



@app.post("/favoriteplayer/", response_model=None, tags=["FavoritePlayer"])
async def create_favoriteplayer(favoriteplayer_data: FavoritePlayerCreate, database: Session = Depends(get_db)) -> FavoritePlayer:

    if favoriteplayer_data.user is not None:
        db_user = database.query(User).filter(User.id == favoriteplayer_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")

    db_favoriteplayer = FavoritePlayer(
        added_at=favoriteplayer_data.added_at,        notify_match=favoriteplayer_data.notify_match,        id=favoriteplayer_data.id,        user_id=favoriteplayer_data.user        )

    database.add(db_favoriteplayer)
    database.commit()
    database.refresh(db_favoriteplayer)

    if favoriteplayer_data.fans:
        # Validate that all Player IDs exist
        for player_id in favoriteplayer_data.fans:
            db_player = database.query(Player).filter(Player.id == player_id).first()
            if not db_player:
                raise HTTPException(status_code=400, detail=f"Player with id {player_id} not found")

        # Update the related entities with the new foreign key
        database.query(Player).filter(Player.id.in_(favoriteplayer_data.fans)).update(
            {Player.joueur_id: db_favoriteplayer.id}, synchronize_session=False
        )
        database.commit()



    fans_ids = database.query(Player.id).filter(Player.joueur_id == db_favoriteplayer.id).all()
    response_data = {
        "favoriteplayer": db_favoriteplayer,
        "fans_ids": [x[0] for x in fans_ids]    }
    return response_data


@app.post("/favoriteplayer/bulk/", response_model=None, tags=["FavoritePlayer"])
async def bulk_create_favoriteplayer(items: list[FavoritePlayerCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple FavoritePlayer entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.user:
                raise ValueError("User ID is required")

            db_favoriteplayer = FavoritePlayer(
                added_at=item_data.added_at,                notify_match=item_data.notify_match,                id=item_data.id,                user_id=item_data.user            )
            database.add(db_favoriteplayer)
            database.flush()  # Get ID without committing
            created_items.append(db_favoriteplayer.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} FavoritePlayer entities"
    }


@app.delete("/favoriteplayer/bulk/", response_model=None, tags=["FavoritePlayer"])
async def bulk_delete_favoriteplayer(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple FavoritePlayer entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_favoriteplayer = database.query(FavoritePlayer).filter(FavoritePlayer.id == item_id).first()
        if db_favoriteplayer:
            database.delete(db_favoriteplayer)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} FavoritePlayer entities"
    }

@app.put("/favoriteplayer/{favoriteplayer_id}/", response_model=None, tags=["FavoritePlayer"])
async def update_favoriteplayer(favoriteplayer_id: int, favoriteplayer_data: FavoritePlayerCreate, database: Session = Depends(get_db)) -> FavoritePlayer:
    db_favoriteplayer = database.query(FavoritePlayer).filter(FavoritePlayer.id == favoriteplayer_id).first()
    if db_favoriteplayer is None:
        raise HTTPException(status_code=404, detail="FavoritePlayer not found")

    setattr(db_favoriteplayer, 'added_at', favoriteplayer_data.added_at)
    setattr(db_favoriteplayer, 'notify_match', favoriteplayer_data.notify_match)
    setattr(db_favoriteplayer, 'id', favoriteplayer_data.id)
    if favoriteplayer_data.user is not None:
        db_user = database.query(User).filter(User.id == favoriteplayer_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_favoriteplayer, 'user_id', favoriteplayer_data.user)
    if favoriteplayer_data.fans is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Player).filter(Player.joueur_id == db_favoriteplayer.id).update(
            {Player.joueur_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if favoriteplayer_data.fans:
            # Validate that all IDs exist
            for player_id in favoriteplayer_data.fans:
                db_player = database.query(Player).filter(Player.id == player_id).first()
                if not db_player:
                    raise HTTPException(status_code=400, detail=f"Player with id {player_id} not found")

            # Update the related entities with the new foreign key
            database.query(Player).filter(Player.id.in_(favoriteplayer_data.fans)).update(
                {Player.joueur_id: db_favoriteplayer.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_favoriteplayer)

    fans_ids = database.query(Player.id).filter(Player.joueur_id == db_favoriteplayer.id).all()
    response_data = {
        "favoriteplayer": db_favoriteplayer,
        "fans_ids": [x[0] for x in fans_ids]    }
    return response_data


@app.delete("/favoriteplayer/{favoriteplayer_id}/", response_model=None, tags=["FavoritePlayer"])
async def delete_favoriteplayer(favoriteplayer_id: int, database: Session = Depends(get_db)):
    db_favoriteplayer = database.query(FavoritePlayer).filter(FavoritePlayer.id == favoriteplayer_id).first()
    if db_favoriteplayer is None:
        raise HTTPException(status_code=404, detail="FavoritePlayer not found")
    database.delete(db_favoriteplayer)
    database.commit()
    return db_favoriteplayer


@app.get("/favoriteplayer/{favoriteplayer_id}/fans/", response_model=None, tags=["FavoritePlayer Relationships"])
async def get_fans_of_favoriteplayer(favoriteplayer_id: int, database: Session = Depends(get_db)):
    """Get all Player entities related to this FavoritePlayer through fans"""
    db_favoriteplayer = database.query(FavoritePlayer).filter(FavoritePlayer.id == favoriteplayer_id).first()
    if db_favoriteplayer is None:
        raise HTTPException(status_code=404, detail="FavoritePlayer not found")

    fans_list = database.query(Player).filter(Player.joueur_id == favoriteplayer_id).all()

    return {
        "favoriteplayer_id": favoriteplayer_id,
        "fans_count": len(fans_list),
        "fans": fans_list
    }





############################################
#
#   FavoriteTeam functions
#
############################################

@app.get("/favoriteteam/", response_model=None, tags=["FavoriteTeam"])
def get_all_favoriteteam(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(FavoriteTeam)
        query = query.options(joinedload(FavoriteTeam.user))
        query = query.options(joinedload(FavoriteTeam.equipe))
        favoriteteam_list = query.all()

        # Serialize with relationships included
        result = []
        for favoriteteam_item in favoriteteam_list:
            item_dict = favoriteteam_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if favoriteteam_item.user:
                related_obj = favoriteteam_item.user
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['user'] = related_dict
            else:
                item_dict['user'] = None
            if favoriteteam_item.equipe:
                related_obj = favoriteteam_item.equipe
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['equipe'] = related_dict
            else:
                item_dict['equipe'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(FavoriteTeam).all()


@app.get("/favoriteteam/count/", response_model=None, tags=["FavoriteTeam"])
def get_count_favoriteteam(database: Session = Depends(get_db)) -> dict:
    """Get the total count of FavoriteTeam entities"""
    count = database.query(FavoriteTeam).count()
    return {"count": count}


@app.get("/favoriteteam/paginated/", response_model=None, tags=["FavoriteTeam"])
def get_paginated_favoriteteam(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of FavoriteTeam entities"""
    total = database.query(FavoriteTeam).count()
    favoriteteam_list = database.query(FavoriteTeam).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": favoriteteam_list
    }


@app.get("/favoriteteam/search/", response_model=None, tags=["FavoriteTeam"])
def search_favoriteteam(
    database: Session = Depends(get_db)
) -> list:
    """Search FavoriteTeam entities by attributes"""
    query = database.query(FavoriteTeam)


    results = query.all()
    return results


@app.get("/favoriteteam/{favoriteteam_id}/", response_model=None, tags=["FavoriteTeam"])
async def get_favoriteteam(favoriteteam_id: int, database: Session = Depends(get_db)) -> FavoriteTeam:
    db_favoriteteam = database.query(FavoriteTeam).filter(FavoriteTeam.id == favoriteteam_id).first()
    if db_favoriteteam is None:
        raise HTTPException(status_code=404, detail="FavoriteTeam not found")

    response_data = {
        "favoriteteam": db_favoriteteam,
}
    return response_data



@app.post("/favoriteteam/", response_model=None, tags=["FavoriteTeam"])
async def create_favoriteteam(favoriteteam_data: FavoriteTeamCreate, database: Session = Depends(get_db)) -> FavoriteTeam:

    if favoriteteam_data.user is not None:
        db_user = database.query(User).filter(User.id == favoriteteam_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if favoriteteam_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == favoriteteam_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
    else:
        raise HTTPException(status_code=400, detail="Team ID is required")

    db_favoriteteam = FavoriteTeam(
        notify_match=favoriteteam_data.notify_match,        id=favoriteteam_data.id,        notify_but=favoriteteam_data.notify_but,        added_at=favoriteteam_data.added_at,        user_id=favoriteteam_data.user,        equipe_id=favoriteteam_data.equipe        )

    database.add(db_favoriteteam)
    database.commit()
    database.refresh(db_favoriteteam)




    return db_favoriteteam


@app.post("/favoriteteam/bulk/", response_model=None, tags=["FavoriteTeam"])
async def bulk_create_favoriteteam(items: list[FavoriteTeamCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple FavoriteTeam entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.user:
                raise ValueError("User ID is required")
            if not item_data.equipe:
                raise ValueError("Team ID is required")

            db_favoriteteam = FavoriteTeam(
                notify_match=item_data.notify_match,                id=item_data.id,                notify_but=item_data.notify_but,                added_at=item_data.added_at,                user_id=item_data.user,                equipe_id=item_data.equipe            )
            database.add(db_favoriteteam)
            database.flush()  # Get ID without committing
            created_items.append(db_favoriteteam.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} FavoriteTeam entities"
    }


@app.delete("/favoriteteam/bulk/", response_model=None, tags=["FavoriteTeam"])
async def bulk_delete_favoriteteam(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple FavoriteTeam entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_favoriteteam = database.query(FavoriteTeam).filter(FavoriteTeam.id == item_id).first()
        if db_favoriteteam:
            database.delete(db_favoriteteam)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} FavoriteTeam entities"
    }

@app.put("/favoriteteam/{favoriteteam_id}/", response_model=None, tags=["FavoriteTeam"])
async def update_favoriteteam(favoriteteam_id: int, favoriteteam_data: FavoriteTeamCreate, database: Session = Depends(get_db)) -> FavoriteTeam:
    db_favoriteteam = database.query(FavoriteTeam).filter(FavoriteTeam.id == favoriteteam_id).first()
    if db_favoriteteam is None:
        raise HTTPException(status_code=404, detail="FavoriteTeam not found")

    setattr(db_favoriteteam, 'notify_match', favoriteteam_data.notify_match)
    setattr(db_favoriteteam, 'id', favoriteteam_data.id)
    setattr(db_favoriteteam, 'notify_but', favoriteteam_data.notify_but)
    setattr(db_favoriteteam, 'added_at', favoriteteam_data.added_at)
    if favoriteteam_data.user is not None:
        db_user = database.query(User).filter(User.id == favoriteteam_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_favoriteteam, 'user_id', favoriteteam_data.user)
    if favoriteteam_data.equipe is not None:
        db_equipe = database.query(Team).filter(Team.id == favoriteteam_data.equipe).first()
        if not db_equipe:
            raise HTTPException(status_code=400, detail="Team not found")
        setattr(db_favoriteteam, 'equipe_id', favoriteteam_data.equipe)
    database.commit()
    database.refresh(db_favoriteteam)

    return db_favoriteteam


@app.delete("/favoriteteam/{favoriteteam_id}/", response_model=None, tags=["FavoriteTeam"])
async def delete_favoriteteam(favoriteteam_id: int, database: Session = Depends(get_db)):
    db_favoriteteam = database.query(FavoriteTeam).filter(FavoriteTeam.id == favoriteteam_id).first()
    if db_favoriteteam is None:
        raise HTTPException(status_code=404, detail="FavoriteTeam not found")
    database.delete(db_favoriteteam)
    database.commit()
    return db_favoriteteam






############################################
#
#   MatchStatistics functions
#
############################################

@app.get("/matchstatistics/", response_model=None, tags=["MatchStatistics"])
def get_all_matchstatistics(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(MatchStatistics)
        query = query.options(joinedload(MatchStatistics.match))
        matchstatistics_list = query.all()

        # Serialize with relationships included
        result = []
        for matchstatistics_item in matchstatistics_list:
            item_dict = matchstatistics_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if matchstatistics_item.match:
                related_obj = matchstatistics_item.match
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['match'] = related_dict
            else:
                item_dict['match'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(MatchStatistics).all()


@app.get("/matchstatistics/count/", response_model=None, tags=["MatchStatistics"])
def get_count_matchstatistics(database: Session = Depends(get_db)) -> dict:
    """Get the total count of MatchStatistics entities"""
    count = database.query(MatchStatistics).count()
    return {"count": count}


@app.get("/matchstatistics/paginated/", response_model=None, tags=["MatchStatistics"])
def get_paginated_matchstatistics(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of MatchStatistics entities"""
    total = database.query(MatchStatistics).count()
    matchstatistics_list = database.query(MatchStatistics).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": matchstatistics_list
    }


@app.get("/matchstatistics/search/", response_model=None, tags=["MatchStatistics"])
def search_matchstatistics(
    database: Session = Depends(get_db)
) -> list:
    """Search MatchStatistics entities by attributes"""
    query = database.query(MatchStatistics)


    results = query.all()
    return results


@app.get("/matchstatistics/{matchstatistics_id}/", response_model=None, tags=["MatchStatistics"])
async def get_matchstatistics(matchstatistics_id: int, database: Session = Depends(get_db)) -> MatchStatistics:
    db_matchstatistics = database.query(MatchStatistics).filter(MatchStatistics.id == matchstatistics_id).first()
    if db_matchstatistics is None:
        raise HTTPException(status_code=404, detail="MatchStatistics not found")

    response_data = {
        "matchstatistics": db_matchstatistics,
}
    return response_data



@app.post("/matchstatistics/", response_model=None, tags=["MatchStatistics"])
async def create_matchstatistics(matchstatistics_data: MatchStatisticsCreate, database: Session = Depends(get_db)) -> MatchStatistics:

    if matchstatistics_data.match is not None:
        db_match = database.query(Match).filter(Match.id == matchstatistics_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
    else:
        raise HTTPException(status_code=400, detail="Match ID is required")

    db_matchstatistics = MatchStatistics(
        transformations_exterieur=matchstatistics_data.transformations_exterieur,        breaks_j1=matchstatistics_data.breaks_j1,        tirs_exterieur=matchstatistics_data.tirs_exterieur,        penalties_dom=matchstatistics_data.penalties_dom,        breaks_j2=matchstatistics_data.breaks_j2,        tirs_cadres_domicile=matchstatistics_data.tirs_cadres_domicile,        penalties_ext=matchstatistics_data.penalties_ext,        sets_j1=matchstatistics_data.sets_j1,        tirs_cadres_exterieur=matchstatistics_data.tirs_cadres_exterieur,        meles_gagnees_dom=matchstatistics_data.meles_gagnees_dom,        sets_j2=matchstatistics_data.sets_j2,        corners_domicile=matchstatistics_data.corners_domicile,        meles_gagnees_ext=matchstatistics_data.meles_gagnees_ext,        corners_exterieur=matchstatistics_data.corners_exterieur,        aces_j1=matchstatistics_data.aces_j1,        fautes_domicile=matchstatistics_data.fautes_domicile,        aces_j2=matchstatistics_data.aces_j2,        fautes_exterieur=matchstatistics_data.fautes_exterieur,        id=matchstatistics_data.id,        doubles_fautes_j1=matchstatistics_data.doubles_fautes_j1,        sport_type=matchstatistics_data.sport_type.value,        essais_domicile=matchstatistics_data.essais_domicile,        doubles_fautes_j2=matchstatistics_data.doubles_fautes_j2,        possession_domicile=matchstatistics_data.possession_domicile,        essais_exterieur=matchstatistics_data.essais_exterieur,        pct_premier_service_j1=matchstatistics_data.pct_premier_service_j1,        possession_exterieur=matchstatistics_data.possession_exterieur,        transformations_domicile=matchstatistics_data.transformations_domicile,        pct_premier_service_j2=matchstatistics_data.pct_premier_service_j2,        tirs_domicile=matchstatistics_data.tirs_domicile,        match_id=matchstatistics_data.match        )

    database.add(db_matchstatistics)
    database.commit()
    database.refresh(db_matchstatistics)




    return db_matchstatistics


@app.post("/matchstatistics/bulk/", response_model=None, tags=["MatchStatistics"])
async def bulk_create_matchstatistics(items: list[MatchStatisticsCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple MatchStatistics entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.match:
                raise ValueError("Match ID is required")

            db_matchstatistics = MatchStatistics(
                transformations_exterieur=item_data.transformations_exterieur,                breaks_j1=item_data.breaks_j1,                tirs_exterieur=item_data.tirs_exterieur,                penalties_dom=item_data.penalties_dom,                breaks_j2=item_data.breaks_j2,                tirs_cadres_domicile=item_data.tirs_cadres_domicile,                penalties_ext=item_data.penalties_ext,                sets_j1=item_data.sets_j1,                tirs_cadres_exterieur=item_data.tirs_cadres_exterieur,                meles_gagnees_dom=item_data.meles_gagnees_dom,                sets_j2=item_data.sets_j2,                corners_domicile=item_data.corners_domicile,                meles_gagnees_ext=item_data.meles_gagnees_ext,                corners_exterieur=item_data.corners_exterieur,                aces_j1=item_data.aces_j1,                fautes_domicile=item_data.fautes_domicile,                aces_j2=item_data.aces_j2,                fautes_exterieur=item_data.fautes_exterieur,                id=item_data.id,                doubles_fautes_j1=item_data.doubles_fautes_j1,                sport_type=item_data.sport_type.value,                essais_domicile=item_data.essais_domicile,                doubles_fautes_j2=item_data.doubles_fautes_j2,                possession_domicile=item_data.possession_domicile,                essais_exterieur=item_data.essais_exterieur,                pct_premier_service_j1=item_data.pct_premier_service_j1,                possession_exterieur=item_data.possession_exterieur,                transformations_domicile=item_data.transformations_domicile,                pct_premier_service_j2=item_data.pct_premier_service_j2,                tirs_domicile=item_data.tirs_domicile,                match_id=item_data.match            )
            database.add(db_matchstatistics)
            database.flush()  # Get ID without committing
            created_items.append(db_matchstatistics.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} MatchStatistics entities"
    }


@app.delete("/matchstatistics/bulk/", response_model=None, tags=["MatchStatistics"])
async def bulk_delete_matchstatistics(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple MatchStatistics entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_matchstatistics = database.query(MatchStatistics).filter(MatchStatistics.id == item_id).first()
        if db_matchstatistics:
            database.delete(db_matchstatistics)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} MatchStatistics entities"
    }

@app.put("/matchstatistics/{matchstatistics_id}/", response_model=None, tags=["MatchStatistics"])
async def update_matchstatistics(matchstatistics_id: int, matchstatistics_data: MatchStatisticsCreate, database: Session = Depends(get_db)) -> MatchStatistics:
    db_matchstatistics = database.query(MatchStatistics).filter(MatchStatistics.id == matchstatistics_id).first()
    if db_matchstatistics is None:
        raise HTTPException(status_code=404, detail="MatchStatistics not found")

    setattr(db_matchstatistics, 'transformations_exterieur', matchstatistics_data.transformations_exterieur)
    setattr(db_matchstatistics, 'breaks_j1', matchstatistics_data.breaks_j1)
    setattr(db_matchstatistics, 'tirs_exterieur', matchstatistics_data.tirs_exterieur)
    setattr(db_matchstatistics, 'penalties_dom', matchstatistics_data.penalties_dom)
    setattr(db_matchstatistics, 'breaks_j2', matchstatistics_data.breaks_j2)
    setattr(db_matchstatistics, 'tirs_cadres_domicile', matchstatistics_data.tirs_cadres_domicile)
    setattr(db_matchstatistics, 'penalties_ext', matchstatistics_data.penalties_ext)
    setattr(db_matchstatistics, 'sets_j1', matchstatistics_data.sets_j1)
    setattr(db_matchstatistics, 'tirs_cadres_exterieur', matchstatistics_data.tirs_cadres_exterieur)
    setattr(db_matchstatistics, 'meles_gagnees_dom', matchstatistics_data.meles_gagnees_dom)
    setattr(db_matchstatistics, 'sets_j2', matchstatistics_data.sets_j2)
    setattr(db_matchstatistics, 'corners_domicile', matchstatistics_data.corners_domicile)
    setattr(db_matchstatistics, 'meles_gagnees_ext', matchstatistics_data.meles_gagnees_ext)
    setattr(db_matchstatistics, 'corners_exterieur', matchstatistics_data.corners_exterieur)
    setattr(db_matchstatistics, 'aces_j1', matchstatistics_data.aces_j1)
    setattr(db_matchstatistics, 'fautes_domicile', matchstatistics_data.fautes_domicile)
    setattr(db_matchstatistics, 'aces_j2', matchstatistics_data.aces_j2)
    setattr(db_matchstatistics, 'fautes_exterieur', matchstatistics_data.fautes_exterieur)
    setattr(db_matchstatistics, 'id', matchstatistics_data.id)
    setattr(db_matchstatistics, 'doubles_fautes_j1', matchstatistics_data.doubles_fautes_j1)
    setattr(db_matchstatistics, 'sport_type', matchstatistics_data.sport_type.value)
    setattr(db_matchstatistics, 'essais_domicile', matchstatistics_data.essais_domicile)
    setattr(db_matchstatistics, 'doubles_fautes_j2', matchstatistics_data.doubles_fautes_j2)
    setattr(db_matchstatistics, 'possession_domicile', matchstatistics_data.possession_domicile)
    setattr(db_matchstatistics, 'essais_exterieur', matchstatistics_data.essais_exterieur)
    setattr(db_matchstatistics, 'pct_premier_service_j1', matchstatistics_data.pct_premier_service_j1)
    setattr(db_matchstatistics, 'possession_exterieur', matchstatistics_data.possession_exterieur)
    setattr(db_matchstatistics, 'transformations_domicile', matchstatistics_data.transformations_domicile)
    setattr(db_matchstatistics, 'pct_premier_service_j2', matchstatistics_data.pct_premier_service_j2)
    setattr(db_matchstatistics, 'tirs_domicile', matchstatistics_data.tirs_domicile)
    if matchstatistics_data.match is not None:
        db_match = database.query(Match).filter(Match.id == matchstatistics_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
        setattr(db_matchstatistics, 'match_id', matchstatistics_data.match)
    database.commit()
    database.refresh(db_matchstatistics)

    return db_matchstatistics


@app.delete("/matchstatistics/{matchstatistics_id}/", response_model=None, tags=["MatchStatistics"])
async def delete_matchstatistics(matchstatistics_id: int, database: Session = Depends(get_db)):
    db_matchstatistics = database.query(MatchStatistics).filter(MatchStatistics.id == matchstatistics_id).first()
    if db_matchstatistics is None:
        raise HTTPException(status_code=404, detail="MatchStatistics not found")
    database.delete(db_matchstatistics)
    database.commit()
    return db_matchstatistics






############################################
#
#   FavoriteCompetition functions
#
############################################

@app.get("/favoritecompetition/", response_model=None, tags=["FavoriteCompetition"])
def get_all_favoritecompetition(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(FavoriteCompetition)
        query = query.options(joinedload(FavoriteCompetition.user))
        query = query.options(joinedload(FavoriteCompetition.competition))
        favoritecompetition_list = query.all()

        # Serialize with relationships included
        result = []
        for favoritecompetition_item in favoritecompetition_list:
            item_dict = favoritecompetition_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if favoritecompetition_item.user:
                related_obj = favoritecompetition_item.user
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['user'] = related_dict
            else:
                item_dict['user'] = None
            if favoritecompetition_item.competition:
                related_obj = favoritecompetition_item.competition
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['competition'] = related_dict
            else:
                item_dict['competition'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(FavoriteCompetition).all()


@app.get("/favoritecompetition/count/", response_model=None, tags=["FavoriteCompetition"])
def get_count_favoritecompetition(database: Session = Depends(get_db)) -> dict:
    """Get the total count of FavoriteCompetition entities"""
    count = database.query(FavoriteCompetition).count()
    return {"count": count}


@app.get("/favoritecompetition/paginated/", response_model=None, tags=["FavoriteCompetition"])
def get_paginated_favoritecompetition(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of FavoriteCompetition entities"""
    total = database.query(FavoriteCompetition).count()
    favoritecompetition_list = database.query(FavoriteCompetition).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": favoritecompetition_list
    }


@app.get("/favoritecompetition/search/", response_model=None, tags=["FavoriteCompetition"])
def search_favoritecompetition(
    database: Session = Depends(get_db)
) -> list:
    """Search FavoriteCompetition entities by attributes"""
    query = database.query(FavoriteCompetition)


    results = query.all()
    return results


@app.get("/favoritecompetition/{favoritecompetition_id}/", response_model=None, tags=["FavoriteCompetition"])
async def get_favoritecompetition(favoritecompetition_id: int, database: Session = Depends(get_db)) -> FavoriteCompetition:
    db_favoritecompetition = database.query(FavoriteCompetition).filter(FavoriteCompetition.id == favoritecompetition_id).first()
    if db_favoritecompetition is None:
        raise HTTPException(status_code=404, detail="FavoriteCompetition not found")

    response_data = {
        "favoritecompetition": db_favoritecompetition,
}
    return response_data



@app.post("/favoritecompetition/", response_model=None, tags=["FavoriteCompetition"])
async def create_favoritecompetition(favoritecompetition_data: FavoriteCompetitionCreate, database: Session = Depends(get_db)) -> FavoriteCompetition:

    if favoritecompetition_data.user is not None:
        db_user = database.query(User).filter(User.id == favoritecompetition_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if favoritecompetition_data.competition is not None:
        db_competition = database.query(Competition).filter(Competition.id == favoritecompetition_data.competition).first()
        if not db_competition:
            raise HTTPException(status_code=400, detail="Competition not found")
    else:
        raise HTTPException(status_code=400, detail="Competition ID is required")

    db_favoritecompetition = FavoriteCompetition(
        id=favoritecompetition_data.id,        notif_active=favoritecompetition_data.notif_active,        added_at=favoritecompetition_data.added_at,        created_at=favoritecompetition_data.created_at,        user_id=favoritecompetition_data.user,        competition_id=favoritecompetition_data.competition        )

    database.add(db_favoritecompetition)
    database.commit()
    database.refresh(db_favoritecompetition)




    return db_favoritecompetition


@app.post("/favoritecompetition/bulk/", response_model=None, tags=["FavoriteCompetition"])
async def bulk_create_favoritecompetition(items: list[FavoriteCompetitionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple FavoriteCompetition entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.user:
                raise ValueError("User ID is required")
            if not item_data.competition:
                raise ValueError("Competition ID is required")

            db_favoritecompetition = FavoriteCompetition(
                id=item_data.id,                notif_active=item_data.notif_active,                added_at=item_data.added_at,                created_at=item_data.created_at,                user_id=item_data.user,                competition_id=item_data.competition            )
            database.add(db_favoritecompetition)
            database.flush()  # Get ID without committing
            created_items.append(db_favoritecompetition.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} FavoriteCompetition entities"
    }


@app.delete("/favoritecompetition/bulk/", response_model=None, tags=["FavoriteCompetition"])
async def bulk_delete_favoritecompetition(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple FavoriteCompetition entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_favoritecompetition = database.query(FavoriteCompetition).filter(FavoriteCompetition.id == item_id).first()
        if db_favoritecompetition:
            database.delete(db_favoritecompetition)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} FavoriteCompetition entities"
    }

@app.put("/favoritecompetition/{favoritecompetition_id}/", response_model=None, tags=["FavoriteCompetition"])
async def update_favoritecompetition(favoritecompetition_id: int, favoritecompetition_data: FavoriteCompetitionCreate, database: Session = Depends(get_db)) -> FavoriteCompetition:
    db_favoritecompetition = database.query(FavoriteCompetition).filter(FavoriteCompetition.id == favoritecompetition_id).first()
    if db_favoritecompetition is None:
        raise HTTPException(status_code=404, detail="FavoriteCompetition not found")

    setattr(db_favoritecompetition, 'id', favoritecompetition_data.id)
    setattr(db_favoritecompetition, 'notif_active', favoritecompetition_data.notif_active)
    setattr(db_favoritecompetition, 'added_at', favoritecompetition_data.added_at)
    setattr(db_favoritecompetition, 'created_at', favoritecompetition_data.created_at)
    if favoritecompetition_data.user is not None:
        db_user = database.query(User).filter(User.id == favoritecompetition_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_favoritecompetition, 'user_id', favoritecompetition_data.user)
    if favoritecompetition_data.competition is not None:
        db_competition = database.query(Competition).filter(Competition.id == favoritecompetition_data.competition).first()
        if not db_competition:
            raise HTTPException(status_code=400, detail="Competition not found")
        setattr(db_favoritecompetition, 'competition_id', favoritecompetition_data.competition)
    database.commit()
    database.refresh(db_favoritecompetition)

    return db_favoritecompetition


@app.delete("/favoritecompetition/{favoritecompetition_id}/", response_model=None, tags=["FavoriteCompetition"])
async def delete_favoritecompetition(favoritecompetition_id: int, database: Session = Depends(get_db)):
    db_favoritecompetition = database.query(FavoriteCompetition).filter(FavoriteCompetition.id == favoritecompetition_id).first()
    if db_favoritecompetition is None:
        raise HTTPException(status_code=404, detail="FavoriteCompetition not found")
    database.delete(db_favoritecompetition)
    database.commit()
    return db_favoritecompetition






############################################
#
#   User functions
#
############################################

@app.get("/user/", response_model=None, tags=["User"])
def get_all_user(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(User)
        user_list = query.all()

        # Serialize with relationships included
        result = []
        for user_item in user_list:
            item_dict = user_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            favoriteteam_list = database.query(FavoriteTeam).filter(FavoriteTeam.user_id == user_item.id).all()
            item_dict['equipes_favorites'] = []
            for favoriteteam_obj in favoriteteam_list:
                favoriteteam_dict = favoriteteam_obj.__dict__.copy()
                favoriteteam_dict.pop('_sa_instance_state', None)
                item_dict['equipes_favorites'].append(favoriteteam_dict)
            favoritecompetition_list = database.query(FavoriteCompetition).filter(FavoriteCompetition.user_id == user_item.id).all()
            item_dict['competitions_favorites'] = []
            for favoritecompetition_obj in favoritecompetition_list:
                favoritecompetition_dict = favoritecompetition_obj.__dict__.copy()
                favoritecompetition_dict.pop('_sa_instance_state', None)
                item_dict['competitions_favorites'].append(favoritecompetition_dict)
            mediafile_list = database.query(MediaFile).filter(MediaFile.uploader_id == user_item.id).all()
            item_dict['medias'] = []
            for mediafile_obj in mediafile_list:
                mediafile_dict = mediafile_obj.__dict__.copy()
                mediafile_dict.pop('_sa_instance_state', None)
                item_dict['medias'].append(mediafile_dict)
            reaction_list = database.query(Reaction).filter(Reaction.user_id == user_item.id).all()
            item_dict['reactions'] = []
            for reaction_obj in reaction_list:
                reaction_dict = reaction_obj.__dict__.copy()
                reaction_dict.pop('_sa_instance_state', None)
                item_dict['reactions'].append(reaction_dict)
            channelmember_list = database.query(ChannelMember).filter(ChannelMember.user_id == user_item.id).all()
            item_dict['canaux_rejoints'] = []
            for channelmember_obj in channelmember_list:
                channelmember_dict = channelmember_obj.__dict__.copy()
                channelmember_dict.pop('_sa_instance_state', None)
                item_dict['canaux_rejoints'].append(channelmember_dict)
            favoriteplayer_list = database.query(FavoritePlayer).filter(FavoritePlayer.user_id == user_item.id).all()
            item_dict['joueurs_favoris'] = []
            for favoriteplayer_obj in favoriteplayer_list:
                favoriteplayer_dict = favoriteplayer_obj.__dict__.copy()
                favoriteplayer_dict.pop('_sa_instance_state', None)
                item_dict['joueurs_favoris'].append(favoriteplayer_dict)
            friendship_list = database.query(Friendship).filter(Friendship.demandeur_id == user_item.id).all()
            item_dict['demandes_envoyees'] = []
            for friendship_obj in friendship_list:
                friendship_dict = friendship_obj.__dict__.copy()
                friendship_dict.pop('_sa_instance_state', None)
                item_dict['demandes_envoyees'].append(friendship_dict)
            friendship_list = database.query(Friendship).filter(Friendship.receveur_id == user_item.id).all()
            item_dict['demandes_recues'] = []
            for friendship_obj in friendship_list:
                friendship_dict = friendship_obj.__dict__.copy()
                friendship_dict.pop('_sa_instance_state', None)
                item_dict['demandes_recues'].append(friendship_dict)
            notification_list = database.query(Notification).filter(Notification.user_id == user_item.id).all()
            item_dict['notifications'] = []
            for notification_obj in notification_list:
                notification_dict = notification_obj.__dict__.copy()
                notification_dict.pop('_sa_instance_state', None)
                item_dict['notifications'].append(notification_dict)
            message_list = database.query(Message).filter(Message.auteur_id == user_item.id).all()
            item_dict['messages'] = []
            for message_obj in message_list:
                message_dict = message_obj.__dict__.copy()
                message_dict.pop('_sa_instance_state', None)
                item_dict['messages'].append(message_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(User).all()


@app.get("/user/count/", response_model=None, tags=["User"])
def get_count_user(database: Session = Depends(get_db)) -> dict:
    """Get the total count of User entities"""
    count = database.query(User).count()
    return {"count": count}


@app.get("/user/paginated/", response_model=None, tags=["User"])
def get_paginated_user(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of User entities"""
    total = database.query(User).count()
    user_list = database.query(User).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": user_list
        }

    result = []
    for user_item in user_list:
        equipes_favorites_ids = database.query(FavoriteTeam.id).filter(FavoriteTeam.user_id == user_item.id).all()
        competitions_favorites_ids = database.query(FavoriteCompetition.id).filter(FavoriteCompetition.user_id == user_item.id).all()
        medias_ids = database.query(MediaFile.id).filter(MediaFile.uploader_id == user_item.id).all()
        reactions_ids = database.query(Reaction.id).filter(Reaction.user_id == user_item.id).all()
        canaux_rejoints_ids = database.query(ChannelMember.id).filter(ChannelMember.user_id == user_item.id).all()
        joueurs_favoris_ids = database.query(FavoritePlayer.id).filter(FavoritePlayer.user_id == user_item.id).all()
        demandes_envoyees_ids = database.query(Friendship.id).filter(Friendship.demandeur_id == user_item.id).all()
        demandes_recues_ids = database.query(Friendship.id).filter(Friendship.receveur_id == user_item.id).all()
        notifications_ids = database.query(Notification.id).filter(Notification.user_id == user_item.id).all()
        messages_ids = database.query(Message.id).filter(Message.auteur_id == user_item.id).all()
        item_data = {
            "user": user_item,
            "equipes_favorites_ids": [x[0] for x in equipes_favorites_ids],            "competitions_favorites_ids": [x[0] for x in competitions_favorites_ids],            "medias_ids": [x[0] for x in medias_ids],            "reactions_ids": [x[0] for x in reactions_ids],            "canaux_rejoints_ids": [x[0] for x in canaux_rejoints_ids],            "joueurs_favoris_ids": [x[0] for x in joueurs_favoris_ids],            "demandes_envoyees_ids": [x[0] for x in demandes_envoyees_ids],            "demandes_recues_ids": [x[0] for x in demandes_recues_ids],            "notifications_ids": [x[0] for x in notifications_ids],            "messages_ids": [x[0] for x in messages_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/user/search/", response_model=None, tags=["User"])
def search_user(
    database: Session = Depends(get_db)
) -> list:
    """Search User entities by attributes"""
    query = database.query(User)


    results = query.all()
    return results


@app.get("/user/{user_id}/", response_model=None, tags=["User"])
async def get_user(user_id: int, database: Session = Depends(get_db)) -> User:
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    equipes_favorites_ids = database.query(FavoriteTeam.id).filter(FavoriteTeam.user_id == db_user.id).all()
    competitions_favorites_ids = database.query(FavoriteCompetition.id).filter(FavoriteCompetition.user_id == db_user.id).all()
    medias_ids = database.query(MediaFile.id).filter(MediaFile.uploader_id == db_user.id).all()
    reactions_ids = database.query(Reaction.id).filter(Reaction.user_id == db_user.id).all()
    canaux_rejoints_ids = database.query(ChannelMember.id).filter(ChannelMember.user_id == db_user.id).all()
    joueurs_favoris_ids = database.query(FavoritePlayer.id).filter(FavoritePlayer.user_id == db_user.id).all()
    demandes_envoyees_ids = database.query(Friendship.id).filter(Friendship.demandeur_id == db_user.id).all()
    demandes_recues_ids = database.query(Friendship.id).filter(Friendship.receveur_id == db_user.id).all()
    notifications_ids = database.query(Notification.id).filter(Notification.user_id == db_user.id).all()
    messages_ids = database.query(Message.id).filter(Message.auteur_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "equipes_favorites_ids": [x[0] for x in equipes_favorites_ids],        "competitions_favorites_ids": [x[0] for x in competitions_favorites_ids],        "medias_ids": [x[0] for x in medias_ids],        "reactions_ids": [x[0] for x in reactions_ids],        "canaux_rejoints_ids": [x[0] for x in canaux_rejoints_ids],        "joueurs_favoris_ids": [x[0] for x in joueurs_favoris_ids],        "demandes_envoyees_ids": [x[0] for x in demandes_envoyees_ids],        "demandes_recues_ids": [x[0] for x in demandes_recues_ids],        "notifications_ids": [x[0] for x in notifications_ids],        "messages_ids": [x[0] for x in messages_ids]}
    return response_data



@app.post("/user/", response_model=None, tags=["User"])
async def create_user(user_data: UserCreate, database: Session = Depends(get_db)) -> User:


    db_user = User(
        username=user_data.username,        bio=user_data.bio,        role=user_data.role.value,        id=user_data.id,        created_at=user_data.created_at,        mot_de_passe_hash=user_data.mot_de_passe_hash,        avatar_url=user_data.avatar_url,        email=user_data.email        )

    database.add(db_user)
    database.commit()
    database.refresh(db_user)

    if user_data.equipes_favorites:
        # Validate that all FavoriteTeam IDs exist
        for favoriteteam_id in user_data.equipes_favorites:
            db_favoriteteam = database.query(FavoriteTeam).filter(FavoriteTeam.id == favoriteteam_id).first()
            if not db_favoriteteam:
                raise HTTPException(status_code=400, detail=f"FavoriteTeam with id {favoriteteam_id} not found")

        # Update the related entities with the new foreign key
        database.query(FavoriteTeam).filter(FavoriteTeam.id.in_(user_data.equipes_favorites)).update(
            {FavoriteTeam.user_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.competitions_favorites:
        # Validate that all FavoriteCompetition IDs exist
        for favoritecompetition_id in user_data.competitions_favorites:
            db_favoritecompetition = database.query(FavoriteCompetition).filter(FavoriteCompetition.id == favoritecompetition_id).first()
            if not db_favoritecompetition:
                raise HTTPException(status_code=400, detail=f"FavoriteCompetition with id {favoritecompetition_id} not found")

        # Update the related entities with the new foreign key
        database.query(FavoriteCompetition).filter(FavoriteCompetition.id.in_(user_data.competitions_favorites)).update(
            {FavoriteCompetition.user_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.medias:
        # Validate that all MediaFile IDs exist
        for mediafile_id in user_data.medias:
            db_mediafile = database.query(MediaFile).filter(MediaFile.id == mediafile_id).first()
            if not db_mediafile:
                raise HTTPException(status_code=400, detail=f"MediaFile with id {mediafile_id} not found")

        # Update the related entities with the new foreign key
        database.query(MediaFile).filter(MediaFile.id.in_(user_data.medias)).update(
            {MediaFile.uploader_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.reactions:
        # Validate that all Reaction IDs exist
        for reaction_id in user_data.reactions:
            db_reaction = database.query(Reaction).filter(Reaction.id == reaction_id).first()
            if not db_reaction:
                raise HTTPException(status_code=400, detail=f"Reaction with id {reaction_id} not found")

        # Update the related entities with the new foreign key
        database.query(Reaction).filter(Reaction.id.in_(user_data.reactions)).update(
            {Reaction.user_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.canaux_rejoints:
        # Validate that all ChannelMember IDs exist
        for channelmember_id in user_data.canaux_rejoints:
            db_channelmember = database.query(ChannelMember).filter(ChannelMember.id == channelmember_id).first()
            if not db_channelmember:
                raise HTTPException(status_code=400, detail=f"ChannelMember with id {channelmember_id} not found")

        # Update the related entities with the new foreign key
        database.query(ChannelMember).filter(ChannelMember.id.in_(user_data.canaux_rejoints)).update(
            {ChannelMember.user_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.joueurs_favoris:
        # Validate that all FavoritePlayer IDs exist
        for favoriteplayer_id in user_data.joueurs_favoris:
            db_favoriteplayer = database.query(FavoritePlayer).filter(FavoritePlayer.id == favoriteplayer_id).first()
            if not db_favoriteplayer:
                raise HTTPException(status_code=400, detail=f"FavoritePlayer with id {favoriteplayer_id} not found")

        # Update the related entities with the new foreign key
        database.query(FavoritePlayer).filter(FavoritePlayer.id.in_(user_data.joueurs_favoris)).update(
            {FavoritePlayer.user_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.demandes_envoyees:
        # Validate that all Friendship IDs exist
        for friendship_id in user_data.demandes_envoyees:
            db_friendship = database.query(Friendship).filter(Friendship.id == friendship_id).first()
            if not db_friendship:
                raise HTTPException(status_code=400, detail=f"Friendship with id {friendship_id} not found")

        # Update the related entities with the new foreign key
        database.query(Friendship).filter(Friendship.id.in_(user_data.demandes_envoyees)).update(
            {Friendship.demandeur_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.demandes_recues:
        # Validate that all Friendship IDs exist
        for friendship_id in user_data.demandes_recues:
            db_friendship = database.query(Friendship).filter(Friendship.id == friendship_id).first()
            if not db_friendship:
                raise HTTPException(status_code=400, detail=f"Friendship with id {friendship_id} not found")

        # Update the related entities with the new foreign key
        database.query(Friendship).filter(Friendship.id.in_(user_data.demandes_recues)).update(
            {Friendship.receveur_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.notifications:
        # Validate that all Notification IDs exist
        for notification_id in user_data.notifications:
            db_notification = database.query(Notification).filter(Notification.id == notification_id).first()
            if not db_notification:
                raise HTTPException(status_code=400, detail=f"Notification with id {notification_id} not found")

        # Update the related entities with the new foreign key
        database.query(Notification).filter(Notification.id.in_(user_data.notifications)).update(
            {Notification.user_id: db_user.id}, synchronize_session=False
        )
        database.commit()
    if user_data.messages:
        # Validate that all Message IDs exist
        for message_id in user_data.messages:
            db_message = database.query(Message).filter(Message.id == message_id).first()
            if not db_message:
                raise HTTPException(status_code=400, detail=f"Message with id {message_id} not found")

        # Update the related entities with the new foreign key
        database.query(Message).filter(Message.id.in_(user_data.messages)).update(
            {Message.auteur_id: db_user.id}, synchronize_session=False
        )
        database.commit()



    equipes_favorites_ids = database.query(FavoriteTeam.id).filter(FavoriteTeam.user_id == db_user.id).all()
    competitions_favorites_ids = database.query(FavoriteCompetition.id).filter(FavoriteCompetition.user_id == db_user.id).all()
    medias_ids = database.query(MediaFile.id).filter(MediaFile.uploader_id == db_user.id).all()
    reactions_ids = database.query(Reaction.id).filter(Reaction.user_id == db_user.id).all()
    canaux_rejoints_ids = database.query(ChannelMember.id).filter(ChannelMember.user_id == db_user.id).all()
    joueurs_favoris_ids = database.query(FavoritePlayer.id).filter(FavoritePlayer.user_id == db_user.id).all()
    demandes_envoyees_ids = database.query(Friendship.id).filter(Friendship.demandeur_id == db_user.id).all()
    demandes_recues_ids = database.query(Friendship.id).filter(Friendship.receveur_id == db_user.id).all()
    notifications_ids = database.query(Notification.id).filter(Notification.user_id == db_user.id).all()
    messages_ids = database.query(Message.id).filter(Message.auteur_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "equipes_favorites_ids": [x[0] for x in equipes_favorites_ids],        "competitions_favorites_ids": [x[0] for x in competitions_favorites_ids],        "medias_ids": [x[0] for x in medias_ids],        "reactions_ids": [x[0] for x in reactions_ids],        "canaux_rejoints_ids": [x[0] for x in canaux_rejoints_ids],        "joueurs_favoris_ids": [x[0] for x in joueurs_favoris_ids],        "demandes_envoyees_ids": [x[0] for x in demandes_envoyees_ids],        "demandes_recues_ids": [x[0] for x in demandes_recues_ids],        "notifications_ids": [x[0] for x in notifications_ids],        "messages_ids": [x[0] for x in messages_ids]    }
    return response_data


@app.post("/user/bulk/", response_model=None, tags=["User"])
async def bulk_create_user(items: list[UserCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple User entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_user = User(
                username=item_data.username,                bio=item_data.bio,                role=item_data.role.value,                id=item_data.id,                created_at=item_data.created_at,                mot_de_passe_hash=item_data.mot_de_passe_hash,                avatar_url=item_data.avatar_url,                email=item_data.email            )
            database.add(db_user)
            database.flush()  # Get ID without committing
            created_items.append(db_user.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} User entities"
    }


@app.delete("/user/bulk/", response_model=None, tags=["User"])
async def bulk_delete_user(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple User entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_user = database.query(User).filter(User.id == item_id).first()
        if db_user:
            database.delete(db_user)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} User entities"
    }

@app.put("/user/{user_id}/", response_model=None, tags=["User"])
async def update_user(user_id: int, user_data: UserCreate, database: Session = Depends(get_db)) -> User:
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    setattr(db_user, 'username', user_data.username)
    setattr(db_user, 'bio', user_data.bio)
    setattr(db_user, 'role', user_data.role.value)
    setattr(db_user, 'id', user_data.id)
    setattr(db_user, 'created_at', user_data.created_at)
    setattr(db_user, 'mot_de_passe_hash', user_data.mot_de_passe_hash)
    setattr(db_user, 'avatar_url', user_data.avatar_url)
    setattr(db_user, 'email', user_data.email)
    if user_data.equipes_favorites is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(FavoriteTeam).filter(FavoriteTeam.user_id == db_user.id).update(
            {FavoriteTeam.user_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.equipes_favorites:
            # Validate that all IDs exist
            for favoriteteam_id in user_data.equipes_favorites:
                db_favoriteteam = database.query(FavoriteTeam).filter(FavoriteTeam.id == favoriteteam_id).first()
                if not db_favoriteteam:
                    raise HTTPException(status_code=400, detail=f"FavoriteTeam with id {favoriteteam_id} not found")

            # Update the related entities with the new foreign key
            database.query(FavoriteTeam).filter(FavoriteTeam.id.in_(user_data.equipes_favorites)).update(
                {FavoriteTeam.user_id: db_user.id}, synchronize_session=False
            )
    if user_data.competitions_favorites is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(FavoriteCompetition).filter(FavoriteCompetition.user_id == db_user.id).update(
            {FavoriteCompetition.user_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.competitions_favorites:
            # Validate that all IDs exist
            for favoritecompetition_id in user_data.competitions_favorites:
                db_favoritecompetition = database.query(FavoriteCompetition).filter(FavoriteCompetition.id == favoritecompetition_id).first()
                if not db_favoritecompetition:
                    raise HTTPException(status_code=400, detail=f"FavoriteCompetition with id {favoritecompetition_id} not found")

            # Update the related entities with the new foreign key
            database.query(FavoriteCompetition).filter(FavoriteCompetition.id.in_(user_data.competitions_favorites)).update(
                {FavoriteCompetition.user_id: db_user.id}, synchronize_session=False
            )
    if user_data.medias is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(MediaFile).filter(MediaFile.uploader_id == db_user.id).update(
            {MediaFile.uploader_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.medias:
            # Validate that all IDs exist
            for mediafile_id in user_data.medias:
                db_mediafile = database.query(MediaFile).filter(MediaFile.id == mediafile_id).first()
                if not db_mediafile:
                    raise HTTPException(status_code=400, detail=f"MediaFile with id {mediafile_id} not found")

            # Update the related entities with the new foreign key
            database.query(MediaFile).filter(MediaFile.id.in_(user_data.medias)).update(
                {MediaFile.uploader_id: db_user.id}, synchronize_session=False
            )
    if user_data.reactions is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Reaction).filter(Reaction.user_id == db_user.id).update(
            {Reaction.user_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.reactions:
            # Validate that all IDs exist
            for reaction_id in user_data.reactions:
                db_reaction = database.query(Reaction).filter(Reaction.id == reaction_id).first()
                if not db_reaction:
                    raise HTTPException(status_code=400, detail=f"Reaction with id {reaction_id} not found")

            # Update the related entities with the new foreign key
            database.query(Reaction).filter(Reaction.id.in_(user_data.reactions)).update(
                {Reaction.user_id: db_user.id}, synchronize_session=False
            )
    if user_data.canaux_rejoints is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ChannelMember).filter(ChannelMember.user_id == db_user.id).update(
            {ChannelMember.user_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.canaux_rejoints:
            # Validate that all IDs exist
            for channelmember_id in user_data.canaux_rejoints:
                db_channelmember = database.query(ChannelMember).filter(ChannelMember.id == channelmember_id).first()
                if not db_channelmember:
                    raise HTTPException(status_code=400, detail=f"ChannelMember with id {channelmember_id} not found")

            # Update the related entities with the new foreign key
            database.query(ChannelMember).filter(ChannelMember.id.in_(user_data.canaux_rejoints)).update(
                {ChannelMember.user_id: db_user.id}, synchronize_session=False
            )
    if user_data.joueurs_favoris is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(FavoritePlayer).filter(FavoritePlayer.user_id == db_user.id).update(
            {FavoritePlayer.user_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.joueurs_favoris:
            # Validate that all IDs exist
            for favoriteplayer_id in user_data.joueurs_favoris:
                db_favoriteplayer = database.query(FavoritePlayer).filter(FavoritePlayer.id == favoriteplayer_id).first()
                if not db_favoriteplayer:
                    raise HTTPException(status_code=400, detail=f"FavoritePlayer with id {favoriteplayer_id} not found")

            # Update the related entities with the new foreign key
            database.query(FavoritePlayer).filter(FavoritePlayer.id.in_(user_data.joueurs_favoris)).update(
                {FavoritePlayer.user_id: db_user.id}, synchronize_session=False
            )
    if user_data.demandes_envoyees is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Friendship).filter(Friendship.demandeur_id == db_user.id).update(
            {Friendship.demandeur_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.demandes_envoyees:
            # Validate that all IDs exist
            for friendship_id in user_data.demandes_envoyees:
                db_friendship = database.query(Friendship).filter(Friendship.id == friendship_id).first()
                if not db_friendship:
                    raise HTTPException(status_code=400, detail=f"Friendship with id {friendship_id} not found")

            # Update the related entities with the new foreign key
            database.query(Friendship).filter(Friendship.id.in_(user_data.demandes_envoyees)).update(
                {Friendship.demandeur_id: db_user.id}, synchronize_session=False
            )
    if user_data.demandes_recues is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Friendship).filter(Friendship.receveur_id == db_user.id).update(
            {Friendship.receveur_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.demandes_recues:
            # Validate that all IDs exist
            for friendship_id in user_data.demandes_recues:
                db_friendship = database.query(Friendship).filter(Friendship.id == friendship_id).first()
                if not db_friendship:
                    raise HTTPException(status_code=400, detail=f"Friendship with id {friendship_id} not found")

            # Update the related entities with the new foreign key
            database.query(Friendship).filter(Friendship.id.in_(user_data.demandes_recues)).update(
                {Friendship.receveur_id: db_user.id}, synchronize_session=False
            )
    if user_data.notifications is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Notification).filter(Notification.user_id == db_user.id).update(
            {Notification.user_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.notifications:
            # Validate that all IDs exist
            for notification_id in user_data.notifications:
                db_notification = database.query(Notification).filter(Notification.id == notification_id).first()
                if not db_notification:
                    raise HTTPException(status_code=400, detail=f"Notification with id {notification_id} not found")

            # Update the related entities with the new foreign key
            database.query(Notification).filter(Notification.id.in_(user_data.notifications)).update(
                {Notification.user_id: db_user.id}, synchronize_session=False
            )
    if user_data.messages is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Message).filter(Message.auteur_id == db_user.id).update(
            {Message.auteur_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if user_data.messages:
            # Validate that all IDs exist
            for message_id in user_data.messages:
                db_message = database.query(Message).filter(Message.id == message_id).first()
                if not db_message:
                    raise HTTPException(status_code=400, detail=f"Message with id {message_id} not found")

            # Update the related entities with the new foreign key
            database.query(Message).filter(Message.id.in_(user_data.messages)).update(
                {Message.auteur_id: db_user.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_user)

    equipes_favorites_ids = database.query(FavoriteTeam.id).filter(FavoriteTeam.user_id == db_user.id).all()
    competitions_favorites_ids = database.query(FavoriteCompetition.id).filter(FavoriteCompetition.user_id == db_user.id).all()
    medias_ids = database.query(MediaFile.id).filter(MediaFile.uploader_id == db_user.id).all()
    reactions_ids = database.query(Reaction.id).filter(Reaction.user_id == db_user.id).all()
    canaux_rejoints_ids = database.query(ChannelMember.id).filter(ChannelMember.user_id == db_user.id).all()
    joueurs_favoris_ids = database.query(FavoritePlayer.id).filter(FavoritePlayer.user_id == db_user.id).all()
    demandes_envoyees_ids = database.query(Friendship.id).filter(Friendship.demandeur_id == db_user.id).all()
    demandes_recues_ids = database.query(Friendship.id).filter(Friendship.receveur_id == db_user.id).all()
    notifications_ids = database.query(Notification.id).filter(Notification.user_id == db_user.id).all()
    messages_ids = database.query(Message.id).filter(Message.auteur_id == db_user.id).all()
    response_data = {
        "user": db_user,
        "equipes_favorites_ids": [x[0] for x in equipes_favorites_ids],        "competitions_favorites_ids": [x[0] for x in competitions_favorites_ids],        "medias_ids": [x[0] for x in medias_ids],        "reactions_ids": [x[0] for x in reactions_ids],        "canaux_rejoints_ids": [x[0] for x in canaux_rejoints_ids],        "joueurs_favoris_ids": [x[0] for x in joueurs_favoris_ids],        "demandes_envoyees_ids": [x[0] for x in demandes_envoyees_ids],        "demandes_recues_ids": [x[0] for x in demandes_recues_ids],        "notifications_ids": [x[0] for x in notifications_ids],        "messages_ids": [x[0] for x in messages_ids]    }
    return response_data


@app.delete("/user/{user_id}/", response_model=None, tags=["User"])
async def delete_user(user_id: int, database: Session = Depends(get_db)):
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    database.delete(db_user)
    database.commit()
    return db_user


@app.get("/user/{user_id}/equipes_favorites/", response_model=None, tags=["User Relationships"])
async def get_equipes_favorites_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all FavoriteTeam entities related to this User through equipes_favorites"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    equipes_favorites_list = database.query(FavoriteTeam).filter(FavoriteTeam.user_id == user_id).all()

    return {
        "user_id": user_id,
        "equipes_favorites_count": len(equipes_favorites_list),
        "equipes_favorites": equipes_favorites_list
    }

@app.get("/user/{user_id}/competitions_favorites/", response_model=None, tags=["User Relationships"])
async def get_competitions_favorites_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all FavoriteCompetition entities related to this User through competitions_favorites"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    competitions_favorites_list = database.query(FavoriteCompetition).filter(FavoriteCompetition.user_id == user_id).all()

    return {
        "user_id": user_id,
        "competitions_favorites_count": len(competitions_favorites_list),
        "competitions_favorites": competitions_favorites_list
    }

@app.get("/user/{user_id}/medias/", response_model=None, tags=["User Relationships"])
async def get_medias_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all MediaFile entities related to this User through medias"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    medias_list = database.query(MediaFile).filter(MediaFile.uploader_id == user_id).all()

    return {
        "user_id": user_id,
        "medias_count": len(medias_list),
        "medias": medias_list
    }

@app.get("/user/{user_id}/reactions/", response_model=None, tags=["User Relationships"])
async def get_reactions_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all Reaction entities related to this User through reactions"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    reactions_list = database.query(Reaction).filter(Reaction.user_id == user_id).all()

    return {
        "user_id": user_id,
        "reactions_count": len(reactions_list),
        "reactions": reactions_list
    }

@app.get("/user/{user_id}/canaux_rejoints/", response_model=None, tags=["User Relationships"])
async def get_canaux_rejoints_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all ChannelMember entities related to this User through canaux_rejoints"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    canaux_rejoints_list = database.query(ChannelMember).filter(ChannelMember.user_id == user_id).all()

    return {
        "user_id": user_id,
        "canaux_rejoints_count": len(canaux_rejoints_list),
        "canaux_rejoints": canaux_rejoints_list
    }

@app.get("/user/{user_id}/joueurs_favoris/", response_model=None, tags=["User Relationships"])
async def get_joueurs_favoris_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all FavoritePlayer entities related to this User through joueurs_favoris"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    joueurs_favoris_list = database.query(FavoritePlayer).filter(FavoritePlayer.user_id == user_id).all()

    return {
        "user_id": user_id,
        "joueurs_favoris_count": len(joueurs_favoris_list),
        "joueurs_favoris": joueurs_favoris_list
    }

@app.get("/user/{user_id}/demandes_envoyees/", response_model=None, tags=["User Relationships"])
async def get_demandes_envoyees_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all Friendship entities related to this User through demandes_envoyees"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    demandes_envoyees_list = database.query(Friendship).filter(Friendship.demandeur_id == user_id).all()

    return {
        "user_id": user_id,
        "demandes_envoyees_count": len(demandes_envoyees_list),
        "demandes_envoyees": demandes_envoyees_list
    }

@app.get("/user/{user_id}/demandes_recues/", response_model=None, tags=["User Relationships"])
async def get_demandes_recues_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all Friendship entities related to this User through demandes_recues"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    demandes_recues_list = database.query(Friendship).filter(Friendship.receveur_id == user_id).all()

    return {
        "user_id": user_id,
        "demandes_recues_count": len(demandes_recues_list),
        "demandes_recues": demandes_recues_list
    }

@app.get("/user/{user_id}/notifications/", response_model=None, tags=["User Relationships"])
async def get_notifications_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all Notification entities related to this User through notifications"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    notifications_list = database.query(Notification).filter(Notification.user_id == user_id).all()

    return {
        "user_id": user_id,
        "notifications_count": len(notifications_list),
        "notifications": notifications_list
    }

@app.get("/user/{user_id}/messages/", response_model=None, tags=["User Relationships"])
async def get_messages_of_user(user_id: int, database: Session = Depends(get_db)):
    """Get all Message entities related to this User through messages"""
    db_user = database.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    messages_list = database.query(Message).filter(Message.auteur_id == user_id).all()

    return {
        "user_id": user_id,
        "messages_count": len(messages_list),
        "messages": messages_list
    }





############################################
#
#   Competition functions
#
############################################

@app.get("/competition/", response_model=None, tags=["Competition"])
def get_all_competition(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Competition)
        query = query.options(joinedload(Competition.sport))
        competition_list = query.all()

        # Serialize with relationships included
        result = []
        for competition_item in competition_list:
            item_dict = competition_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if competition_item.sport:
                related_obj = competition_item.sport
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['sport'] = related_dict
            else:
                item_dict['sport'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            team_list = database.query(Team).join(competition_team, Team.id == competition_team.c.equipes).filter(competition_team.c.competitions == competition_item.id).all()
            item_dict['equipes'] = []
            for team_obj in team_list:
                team_dict = team_obj.__dict__.copy()
                team_dict.pop('_sa_instance_state', None)
                item_dict['equipes'].append(team_dict)
            standing_list = database.query(Standing).filter(Standing.competition_id == competition_item.id).all()
            item_dict['classement'] = []
            for standing_obj in standing_list:
                standing_dict = standing_obj.__dict__.copy()
                standing_dict.pop('_sa_instance_state', None)
                item_dict['classement'].append(standing_dict)
            match_list = database.query(Match).filter(Match.competition_id == competition_item.id).all()
            item_dict['matchs'] = []
            for match_obj in match_list:
                match_dict = match_obj.__dict__.copy()
                match_dict.pop('_sa_instance_state', None)
                item_dict['matchs'].append(match_dict)
            tournamentround_list = database.query(TournamentRound).filter(TournamentRound.competition_id == competition_item.id).all()
            item_dict['tours'] = []
            for tournamentround_obj in tournamentround_list:
                tournamentround_dict = tournamentround_obj.__dict__.copy()
                tournamentround_dict.pop('_sa_instance_state', None)
                item_dict['tours'].append(tournamentround_dict)
            favoritecompetition_list = database.query(FavoriteCompetition).filter(FavoriteCompetition.competition_id == competition_item.id).all()
            item_dict['abonnes'] = []
            for favoritecompetition_obj in favoritecompetition_list:
                favoritecompetition_dict = favoritecompetition_obj.__dict__.copy()
                favoritecompetition_dict.pop('_sa_instance_state', None)
                item_dict['abonnes'].append(favoritecompetition_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Competition).all()


@app.get("/competition/count/", response_model=None, tags=["Competition"])
def get_count_competition(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Competition entities"""
    count = database.query(Competition).count()
    return {"count": count}


@app.get("/competition/paginated/", response_model=None, tags=["Competition"])
def get_paginated_competition(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Competition entities"""
    total = database.query(Competition).count()
    competition_list = database.query(Competition).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": competition_list
        }

    result = []
    for competition_item in competition_list:
        team_ids = database.query(competition_team.c.equipes).filter(competition_team.c.competitions == competition_item.id).all()
        classement_ids = database.query(Standing.id).filter(Standing.competition_id == competition_item.id).all()
        matchs_ids = database.query(Match.id).filter(Match.competition_id == competition_item.id).all()
        tours_ids = database.query(TournamentRound.id).filter(TournamentRound.competition_id == competition_item.id).all()
        abonnes_ids = database.query(FavoriteCompetition.id).filter(FavoriteCompetition.competition_id == competition_item.id).all()
        item_data = {
            "competition": competition_item,
            "team_ids": [x[0] for x in team_ids],
            "classement_ids": [x[0] for x in classement_ids],            "matchs_ids": [x[0] for x in matchs_ids],            "tours_ids": [x[0] for x in tours_ids],            "abonnes_ids": [x[0] for x in abonnes_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/competition/search/", response_model=None, tags=["Competition"])
def search_competition(
    database: Session = Depends(get_db)
) -> list:
    """Search Competition entities by attributes"""
    query = database.query(Competition)


    results = query.all()
    return results


@app.get("/competition/{competition_id}/", response_model=None, tags=["Competition"])
async def get_competition(competition_id: int, database: Session = Depends(get_db)) -> Competition:
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    team_ids = database.query(competition_team.c.equipes).filter(competition_team.c.competitions == db_competition.id).all()
    classement_ids = database.query(Standing.id).filter(Standing.competition_id == db_competition.id).all()
    matchs_ids = database.query(Match.id).filter(Match.competition_id == db_competition.id).all()
    tours_ids = database.query(TournamentRound.id).filter(TournamentRound.competition_id == db_competition.id).all()
    abonnes_ids = database.query(FavoriteCompetition.id).filter(FavoriteCompetition.competition_id == db_competition.id).all()
    response_data = {
        "competition": db_competition,
        "team_ids": [x[0] for x in team_ids],
        "classement_ids": [x[0] for x in classement_ids],        "matchs_ids": [x[0] for x in matchs_ids],        "tours_ids": [x[0] for x in tours_ids],        "abonnes_ids": [x[0] for x in abonnes_ids]}
    return response_data



@app.post("/competition/", response_model=None, tags=["Competition"])
async def create_competition(competition_data: CompetitionCreate, database: Session = Depends(get_db)) -> Competition:

    if competition_data.sport is not None:
        db_sport = database.query(Sport).filter(Sport.id == competition_data.sport).first()
        if not db_sport:
            raise HTTPException(status_code=400, detail="Sport not found")
    else:
        raise HTTPException(status_code=400, detail="Sport ID is required")
    if competition_data.equipes:
        for id in competition_data.equipes:
            # Entity already validated before creation
            db_team = database.query(Team).filter(Team.id == id).first()
            if not db_team:
                raise HTTPException(status_code=404, detail=f"Team with ID {id} not found")

    db_competition = Competition(
        logo_url=competition_data.logo_url,        saison=competition_data.saison,        date_fin=competition_data.date_fin,        format=competition_data.format.value,        nom=competition_data.nom,        statut=competition_data.statut.value,        id=competition_data.id,        pays=competition_data.pays,        date_debut=competition_data.date_debut,        sport_id=competition_data.sport        )

    database.add(db_competition)
    database.commit()
    database.refresh(db_competition)

    if competition_data.classement:
        # Validate that all Standing IDs exist
        for standing_id in competition_data.classement:
            db_standing = database.query(Standing).filter(Standing.id == standing_id).first()
            if not db_standing:
                raise HTTPException(status_code=400, detail=f"Standing with id {standing_id} not found")

        # Update the related entities with the new foreign key
        database.query(Standing).filter(Standing.id.in_(competition_data.classement)).update(
            {Standing.competition_id: db_competition.id}, synchronize_session=False
        )
        database.commit()
    if competition_data.matchs:
        # Validate that all Match IDs exist
        for match_id in competition_data.matchs:
            db_match = database.query(Match).filter(Match.id == match_id).first()
            if not db_match:
                raise HTTPException(status_code=400, detail=f"Match with id {match_id} not found")

        # Update the related entities with the new foreign key
        database.query(Match).filter(Match.id.in_(competition_data.matchs)).update(
            {Match.competition_id: db_competition.id}, synchronize_session=False
        )
        database.commit()
    if competition_data.tours:
        # Validate that all TournamentRound IDs exist
        for tournamentround_id in competition_data.tours:
            db_tournamentround = database.query(TournamentRound).filter(TournamentRound.id == tournamentround_id).first()
            if not db_tournamentround:
                raise HTTPException(status_code=400, detail=f"TournamentRound with id {tournamentround_id} not found")

        # Update the related entities with the new foreign key
        database.query(TournamentRound).filter(TournamentRound.id.in_(competition_data.tours)).update(
            {TournamentRound.competition_id: db_competition.id}, synchronize_session=False
        )
        database.commit()
    if competition_data.abonnes:
        # Validate that all FavoriteCompetition IDs exist
        for favoritecompetition_id in competition_data.abonnes:
            db_favoritecompetition = database.query(FavoriteCompetition).filter(FavoriteCompetition.id == favoritecompetition_id).first()
            if not db_favoritecompetition:
                raise HTTPException(status_code=400, detail=f"FavoriteCompetition with id {favoritecompetition_id} not found")

        # Update the related entities with the new foreign key
        database.query(FavoriteCompetition).filter(FavoriteCompetition.id.in_(competition_data.abonnes)).update(
            {FavoriteCompetition.competition_id: db_competition.id}, synchronize_session=False
        )
        database.commit()

    if competition_data.equipes:
        for id in competition_data.equipes:
            # Entity already validated before creation
            db_team = database.query(Team).filter(Team.id == id).first()
            # Create the association
            association = competition_team.insert().values(competitions=db_competition.id, equipes=db_team.id)
            database.execute(association)
            database.commit()


    team_ids = database.query(competition_team.c.equipes).filter(competition_team.c.competitions == db_competition.id).all()
    classement_ids = database.query(Standing.id).filter(Standing.competition_id == db_competition.id).all()
    matchs_ids = database.query(Match.id).filter(Match.competition_id == db_competition.id).all()
    tours_ids = database.query(TournamentRound.id).filter(TournamentRound.competition_id == db_competition.id).all()
    abonnes_ids = database.query(FavoriteCompetition.id).filter(FavoriteCompetition.competition_id == db_competition.id).all()
    response_data = {
        "competition": db_competition,
        "team_ids": [x[0] for x in team_ids],
        "classement_ids": [x[0] for x in classement_ids],        "matchs_ids": [x[0] for x in matchs_ids],        "tours_ids": [x[0] for x in tours_ids],        "abonnes_ids": [x[0] for x in abonnes_ids]    }
    return response_data


@app.post("/competition/bulk/", response_model=None, tags=["Competition"])
async def bulk_create_competition(items: list[CompetitionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Competition entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.sport:
                raise ValueError("Sport ID is required")

            db_competition = Competition(
                logo_url=item_data.logo_url,                saison=item_data.saison,                date_fin=item_data.date_fin,                format=item_data.format.value,                nom=item_data.nom,                statut=item_data.statut.value,                id=item_data.id,                pays=item_data.pays,                date_debut=item_data.date_debut,                sport_id=item_data.sport            )
            database.add(db_competition)
            database.flush()  # Get ID without committing
            created_items.append(db_competition.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Competition entities"
    }


@app.delete("/competition/bulk/", response_model=None, tags=["Competition"])
async def bulk_delete_competition(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Competition entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_competition = database.query(Competition).filter(Competition.id == item_id).first()
        if db_competition:
            database.delete(db_competition)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Competition entities"
    }

@app.put("/competition/{competition_id}/", response_model=None, tags=["Competition"])
async def update_competition(competition_id: int, competition_data: CompetitionCreate, database: Session = Depends(get_db)) -> Competition:
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    setattr(db_competition, 'logo_url', competition_data.logo_url)
    setattr(db_competition, 'saison', competition_data.saison)
    setattr(db_competition, 'date_fin', competition_data.date_fin)
    setattr(db_competition, 'format', competition_data.format.value)
    setattr(db_competition, 'nom', competition_data.nom)
    setattr(db_competition, 'statut', competition_data.statut.value)
    setattr(db_competition, 'id', competition_data.id)
    setattr(db_competition, 'pays', competition_data.pays)
    setattr(db_competition, 'date_debut', competition_data.date_debut)
    if competition_data.sport is not None:
        db_sport = database.query(Sport).filter(Sport.id == competition_data.sport).first()
        if not db_sport:
            raise HTTPException(status_code=400, detail="Sport not found")
        setattr(db_competition, 'sport_id', competition_data.sport)
    if competition_data.classement is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Standing).filter(Standing.competition_id == db_competition.id).update(
            {Standing.competition_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if competition_data.classement:
            # Validate that all IDs exist
            for standing_id in competition_data.classement:
                db_standing = database.query(Standing).filter(Standing.id == standing_id).first()
                if not db_standing:
                    raise HTTPException(status_code=400, detail=f"Standing with id {standing_id} not found")

            # Update the related entities with the new foreign key
            database.query(Standing).filter(Standing.id.in_(competition_data.classement)).update(
                {Standing.competition_id: db_competition.id}, synchronize_session=False
            )
    if competition_data.matchs is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Match).filter(Match.competition_id == db_competition.id).update(
            {Match.competition_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if competition_data.matchs:
            # Validate that all IDs exist
            for match_id in competition_data.matchs:
                db_match = database.query(Match).filter(Match.id == match_id).first()
                if not db_match:
                    raise HTTPException(status_code=400, detail=f"Match with id {match_id} not found")

            # Update the related entities with the new foreign key
            database.query(Match).filter(Match.id.in_(competition_data.matchs)).update(
                {Match.competition_id: db_competition.id}, synchronize_session=False
            )
    if competition_data.tours is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(TournamentRound).filter(TournamentRound.competition_id == db_competition.id).update(
            {TournamentRound.competition_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if competition_data.tours:
            # Validate that all IDs exist
            for tournamentround_id in competition_data.tours:
                db_tournamentround = database.query(TournamentRound).filter(TournamentRound.id == tournamentround_id).first()
                if not db_tournamentround:
                    raise HTTPException(status_code=400, detail=f"TournamentRound with id {tournamentround_id} not found")

            # Update the related entities with the new foreign key
            database.query(TournamentRound).filter(TournamentRound.id.in_(competition_data.tours)).update(
                {TournamentRound.competition_id: db_competition.id}, synchronize_session=False
            )
    if competition_data.abonnes is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(FavoriteCompetition).filter(FavoriteCompetition.competition_id == db_competition.id).update(
            {FavoriteCompetition.competition_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if competition_data.abonnes:
            # Validate that all IDs exist
            for favoritecompetition_id in competition_data.abonnes:
                db_favoritecompetition = database.query(FavoriteCompetition).filter(FavoriteCompetition.id == favoritecompetition_id).first()
                if not db_favoritecompetition:
                    raise HTTPException(status_code=400, detail=f"FavoriteCompetition with id {favoritecompetition_id} not found")

            # Update the related entities with the new foreign key
            database.query(FavoriteCompetition).filter(FavoriteCompetition.id.in_(competition_data.abonnes)).update(
                {FavoriteCompetition.competition_id: db_competition.id}, synchronize_session=False
            )
    existing_team_ids = [assoc.equipes for assoc in database.execute(
        competition_team.select().where(competition_team.c.competitions == db_competition.id))]

    teams_to_remove = set(existing_team_ids) - set(competition_data.equipes)
    for team_id in teams_to_remove:
        association = competition_team.delete().where(
            (competition_team.c.competitions == db_competition.id) & (competition_team.c.equipes == team_id))
        database.execute(association)

    new_team_ids = set(competition_data.equipes) - set(existing_team_ids)
    for team_id in new_team_ids:
        db_team = database.query(Team).filter(Team.id == team_id).first()
        if db_team is None:
            raise HTTPException(status_code=404, detail=f"Team with ID {team_id} not found")
        association = competition_team.insert().values(equipes=db_team.id, competitions=db_competition.id)
        database.execute(association)
    database.commit()
    database.refresh(db_competition)

    team_ids = database.query(competition_team.c.equipes).filter(competition_team.c.competitions == db_competition.id).all()
    classement_ids = database.query(Standing.id).filter(Standing.competition_id == db_competition.id).all()
    matchs_ids = database.query(Match.id).filter(Match.competition_id == db_competition.id).all()
    tours_ids = database.query(TournamentRound.id).filter(TournamentRound.competition_id == db_competition.id).all()
    abonnes_ids = database.query(FavoriteCompetition.id).filter(FavoriteCompetition.competition_id == db_competition.id).all()
    response_data = {
        "competition": db_competition,
        "team_ids": [x[0] for x in team_ids],
        "classement_ids": [x[0] for x in classement_ids],        "matchs_ids": [x[0] for x in matchs_ids],        "tours_ids": [x[0] for x in tours_ids],        "abonnes_ids": [x[0] for x in abonnes_ids]    }
    return response_data


@app.delete("/competition/{competition_id}/", response_model=None, tags=["Competition"])
async def delete_competition(competition_id: int, database: Session = Depends(get_db)):
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    database.delete(db_competition)
    database.commit()
    return db_competition

@app.post("/competition/{competition_id}/equipes/{team_id}/", response_model=None, tags=["Competition Relationships"])
async def add_equipes_to_competition(competition_id: int, team_id: int, database: Session = Depends(get_db)):
    """Add a Team to this Competition's equipes relationship"""
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    db_team = database.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    # Check if relationship already exists
    existing = database.query(competition_team).filter(
        (competition_team.c.competitions == competition_id) &
        (competition_team.c.equipes == team_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = competition_team.insert().values(competitions=competition_id, equipes=team_id)
    database.execute(association)
    database.commit()

    return {"message": "Team added to equipes successfully"}


@app.delete("/competition/{competition_id}/equipes/{team_id}/", response_model=None, tags=["Competition Relationships"])
async def remove_equipes_from_competition(competition_id: int, team_id: int, database: Session = Depends(get_db)):
    """Remove a Team from this Competition's equipes relationship"""
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    # Check if relationship exists
    existing = database.query(competition_team).filter(
        (competition_team.c.competitions == competition_id) &
        (competition_team.c.equipes == team_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = competition_team.delete().where(
        (competition_team.c.competitions == competition_id) &
        (competition_team.c.equipes == team_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Team removed from equipes successfully"}


@app.get("/competition/{competition_id}/equipes/", response_model=None, tags=["Competition Relationships"])
async def get_equipes_of_competition(competition_id: int, database: Session = Depends(get_db)):
    """Get all Team entities related to this Competition through equipes"""
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    team_ids = database.query(competition_team.c.equipes).filter(competition_team.c.competitions == competition_id).all()
    team_list = database.query(Team).filter(Team.id.in_([id[0] for id in team_ids])).all()

    return {
        "competition_id": competition_id,
        "equipes_count": len(team_list),
        "equipes": team_list
    }


@app.get("/competition/{competition_id}/classement/", response_model=None, tags=["Competition Relationships"])
async def get_classement_of_competition(competition_id: int, database: Session = Depends(get_db)):
    """Get all Standing entities related to this Competition through classement"""
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    classement_list = database.query(Standing).filter(Standing.competition_id == competition_id).all()

    return {
        "competition_id": competition_id,
        "classement_count": len(classement_list),
        "classement": classement_list
    }

@app.get("/competition/{competition_id}/matchs/", response_model=None, tags=["Competition Relationships"])
async def get_matchs_of_competition(competition_id: int, database: Session = Depends(get_db)):
    """Get all Match entities related to this Competition through matchs"""
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    matchs_list = database.query(Match).filter(Match.competition_id == competition_id).all()

    return {
        "competition_id": competition_id,
        "matchs_count": len(matchs_list),
        "matchs": matchs_list
    }

@app.get("/competition/{competition_id}/tours/", response_model=None, tags=["Competition Relationships"])
async def get_tours_of_competition(competition_id: int, database: Session = Depends(get_db)):
    """Get all TournamentRound entities related to this Competition through tours"""
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    tours_list = database.query(TournamentRound).filter(TournamentRound.competition_id == competition_id).all()

    return {
        "competition_id": competition_id,
        "tours_count": len(tours_list),
        "tours": tours_list
    }

@app.get("/competition/{competition_id}/abonnes/", response_model=None, tags=["Competition Relationships"])
async def get_abonnes_of_competition(competition_id: int, database: Session = Depends(get_db)):
    """Get all FavoriteCompetition entities related to this Competition through abonnes"""
    db_competition = database.query(Competition).filter(Competition.id == competition_id).first()
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")

    abonnes_list = database.query(FavoriteCompetition).filter(FavoriteCompetition.competition_id == competition_id).all()

    return {
        "competition_id": competition_id,
        "abonnes_count": len(abonnes_list),
        "abonnes": abonnes_list
    }





############################################
#
#   ChannelMember functions
#
############################################

@app.get("/channelmember/", response_model=None, tags=["ChannelMember"])
def get_all_channelmember(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ChannelMember)
        query = query.options(joinedload(ChannelMember.user))
        query = query.options(joinedload(ChannelMember.canal))
        channelmember_list = query.all()

        # Serialize with relationships included
        result = []
        for channelmember_item in channelmember_list:
            item_dict = channelmember_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if channelmember_item.user:
                related_obj = channelmember_item.user
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['user'] = related_dict
            else:
                item_dict['user'] = None
            if channelmember_item.canal:
                related_obj = channelmember_item.canal
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['canal'] = related_dict
            else:
                item_dict['canal'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ChannelMember).all()


@app.get("/channelmember/count/", response_model=None, tags=["ChannelMember"])
def get_count_channelmember(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ChannelMember entities"""
    count = database.query(ChannelMember).count()
    return {"count": count}


@app.get("/channelmember/paginated/", response_model=None, tags=["ChannelMember"])
def get_paginated_channelmember(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ChannelMember entities"""
    total = database.query(ChannelMember).count()
    channelmember_list = database.query(ChannelMember).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": channelmember_list
    }


@app.get("/channelmember/search/", response_model=None, tags=["ChannelMember"])
def search_channelmember(
    database: Session = Depends(get_db)
) -> list:
    """Search ChannelMember entities by attributes"""
    query = database.query(ChannelMember)


    results = query.all()
    return results


@app.get("/channelmember/{channelmember_id}/", response_model=None, tags=["ChannelMember"])
async def get_channelmember(channelmember_id: int, database: Session = Depends(get_db)) -> ChannelMember:
    db_channelmember = database.query(ChannelMember).filter(ChannelMember.id == channelmember_id).first()
    if db_channelmember is None:
        raise HTTPException(status_code=404, detail="ChannelMember not found")

    response_data = {
        "channelmember": db_channelmember,
}
    return response_data



@app.post("/channelmember/", response_model=None, tags=["ChannelMember"])
async def create_channelmember(channelmember_data: ChannelMemberCreate, database: Session = Depends(get_db)) -> ChannelMember:

    if channelmember_data.user is not None:
        db_user = database.query(User).filter(User.id == channelmember_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User ID is required")
    if channelmember_data.canal is not None:
        db_canal = database.query(Channel).filter(Channel.id == channelmember_data.canal).first()
        if not db_canal:
            raise HTTPException(status_code=400, detail="Channel not found")
    else:
        raise HTTPException(status_code=400, detail="Channel ID is required")

    db_channelmember = ChannelMember(
        is_admin=channelmember_data.is_admin,        last_read_at=channelmember_data.last_read_at,        id=channelmember_data.id,        joined_at=channelmember_data.joined_at,        user_id=channelmember_data.user,        canal_id=channelmember_data.canal        )

    database.add(db_channelmember)
    database.commit()
    database.refresh(db_channelmember)




    return db_channelmember


@app.post("/channelmember/bulk/", response_model=None, tags=["ChannelMember"])
async def bulk_create_channelmember(items: list[ChannelMemberCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ChannelMember entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.user:
                raise ValueError("User ID is required")
            if not item_data.canal:
                raise ValueError("Channel ID is required")

            db_channelmember = ChannelMember(
                is_admin=item_data.is_admin,                last_read_at=item_data.last_read_at,                id=item_data.id,                joined_at=item_data.joined_at,                user_id=item_data.user,                canal_id=item_data.canal            )
            database.add(db_channelmember)
            database.flush()  # Get ID without committing
            created_items.append(db_channelmember.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ChannelMember entities"
    }


@app.delete("/channelmember/bulk/", response_model=None, tags=["ChannelMember"])
async def bulk_delete_channelmember(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ChannelMember entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_channelmember = database.query(ChannelMember).filter(ChannelMember.id == item_id).first()
        if db_channelmember:
            database.delete(db_channelmember)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ChannelMember entities"
    }

@app.put("/channelmember/{channelmember_id}/", response_model=None, tags=["ChannelMember"])
async def update_channelmember(channelmember_id: int, channelmember_data: ChannelMemberCreate, database: Session = Depends(get_db)) -> ChannelMember:
    db_channelmember = database.query(ChannelMember).filter(ChannelMember.id == channelmember_id).first()
    if db_channelmember is None:
        raise HTTPException(status_code=404, detail="ChannelMember not found")

    setattr(db_channelmember, 'is_admin', channelmember_data.is_admin)
    setattr(db_channelmember, 'last_read_at', channelmember_data.last_read_at)
    setattr(db_channelmember, 'id', channelmember_data.id)
    setattr(db_channelmember, 'joined_at', channelmember_data.joined_at)
    if channelmember_data.user is not None:
        db_user = database.query(User).filter(User.id == channelmember_data.user).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        setattr(db_channelmember, 'user_id', channelmember_data.user)
    if channelmember_data.canal is not None:
        db_canal = database.query(Channel).filter(Channel.id == channelmember_data.canal).first()
        if not db_canal:
            raise HTTPException(status_code=400, detail="Channel not found")
        setattr(db_channelmember, 'canal_id', channelmember_data.canal)
    database.commit()
    database.refresh(db_channelmember)

    return db_channelmember


@app.delete("/channelmember/{channelmember_id}/", response_model=None, tags=["ChannelMember"])
async def delete_channelmember(channelmember_id: int, database: Session = Depends(get_db)):
    db_channelmember = database.query(ChannelMember).filter(ChannelMember.id == channelmember_id).first()
    if db_channelmember is None:
        raise HTTPException(status_code=404, detail="ChannelMember not found")
    database.delete(db_channelmember)
    database.commit()
    return db_channelmember






############################################
#
#   Channel functions
#
############################################

@app.get("/channel/", response_model=None, tags=["Channel"])
def get_all_channel(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Channel)
        query = query.options(joinedload(Channel.match))
        channel_list = query.all()

        # Serialize with relationships included
        result = []
        for channel_item in channel_list:
            item_dict = channel_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if channel_item.match:
                related_obj = channel_item.match
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['match'] = related_dict
            else:
                item_dict['match'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            channelmember_list = database.query(ChannelMember).filter(ChannelMember.canal_id == channel_item.id).all()
            item_dict['membres'] = []
            for channelmember_obj in channelmember_list:
                channelmember_dict = channelmember_obj.__dict__.copy()
                channelmember_dict.pop('_sa_instance_state', None)
                item_dict['membres'].append(channelmember_dict)
            message_list = database.query(Message).filter(Message.canal_id == channel_item.id).all()
            item_dict['messages'] = []
            for message_obj in message_list:
                message_dict = message_obj.__dict__.copy()
                message_dict.pop('_sa_instance_state', None)
                item_dict['messages'].append(message_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Channel).all()


@app.get("/channel/count/", response_model=None, tags=["Channel"])
def get_count_channel(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Channel entities"""
    count = database.query(Channel).count()
    return {"count": count}


@app.get("/channel/paginated/", response_model=None, tags=["Channel"])
def get_paginated_channel(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Channel entities"""
    total = database.query(Channel).count()
    channel_list = database.query(Channel).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": channel_list
        }

    result = []
    for channel_item in channel_list:
        membres_ids = database.query(ChannelMember.id).filter(ChannelMember.canal_id == channel_item.id).all()
        messages_ids = database.query(Message.id).filter(Message.canal_id == channel_item.id).all()
        item_data = {
            "channel": channel_item,
            "membres_ids": [x[0] for x in membres_ids],            "messages_ids": [x[0] for x in messages_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/channel/search/", response_model=None, tags=["Channel"])
def search_channel(
    database: Session = Depends(get_db)
) -> list:
    """Search Channel entities by attributes"""
    query = database.query(Channel)


    results = query.all()
    return results


@app.get("/channel/{channel_id}/", response_model=None, tags=["Channel"])
async def get_channel(channel_id: int, database: Session = Depends(get_db)) -> Channel:
    db_channel = database.query(Channel).filter(Channel.id == channel_id).first()
    if db_channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    membres_ids = database.query(ChannelMember.id).filter(ChannelMember.canal_id == db_channel.id).all()
    messages_ids = database.query(Message.id).filter(Message.canal_id == db_channel.id).all()
    response_data = {
        "channel": db_channel,
        "membres_ids": [x[0] for x in membres_ids],        "messages_ids": [x[0] for x in messages_ids]}
    return response_data



@app.post("/channel/", response_model=None, tags=["Channel"])
async def create_channel(channel_data: ChannelCreate, database: Session = Depends(get_db)) -> Channel:

    if channel_data.match :
        db_match = database.query(Match).filter(Match.id == channel_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")

    db_channel = Channel(
        type=channel_data.type.value,        id=channel_data.id,        is_live=channel_data.is_live,        created_at=channel_data.created_at,        nom=channel_data.nom,        match_id=channel_data.match        )

    database.add(db_channel)
    database.commit()
    database.refresh(db_channel)

    if channel_data.membres:
        # Validate that all ChannelMember IDs exist
        for channelmember_id in channel_data.membres:
            db_channelmember = database.query(ChannelMember).filter(ChannelMember.id == channelmember_id).first()
            if not db_channelmember:
                raise HTTPException(status_code=400, detail=f"ChannelMember with id {channelmember_id} not found")

        # Update the related entities with the new foreign key
        database.query(ChannelMember).filter(ChannelMember.id.in_(channel_data.membres)).update(
            {ChannelMember.canal_id: db_channel.id}, synchronize_session=False
        )
        database.commit()
    if channel_data.messages:
        # Validate that all Message IDs exist
        for message_id in channel_data.messages:
            db_message = database.query(Message).filter(Message.id == message_id).first()
            if not db_message:
                raise HTTPException(status_code=400, detail=f"Message with id {message_id} not found")

        # Update the related entities with the new foreign key
        database.query(Message).filter(Message.id.in_(channel_data.messages)).update(
            {Message.canal_id: db_channel.id}, synchronize_session=False
        )
        database.commit()



    membres_ids = database.query(ChannelMember.id).filter(ChannelMember.canal_id == db_channel.id).all()
    messages_ids = database.query(Message.id).filter(Message.canal_id == db_channel.id).all()
    response_data = {
        "channel": db_channel,
        "membres_ids": [x[0] for x in membres_ids],        "messages_ids": [x[0] for x in messages_ids]    }
    return response_data


@app.post("/channel/bulk/", response_model=None, tags=["Channel"])
async def bulk_create_channel(items: list[ChannelCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Channel entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_channel = Channel(
                type=item_data.type.value,                id=item_data.id,                is_live=item_data.is_live,                created_at=item_data.created_at,                nom=item_data.nom,                match_id=item_data.match            )
            database.add(db_channel)
            database.flush()  # Get ID without committing
            created_items.append(db_channel.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Channel entities"
    }


@app.delete("/channel/bulk/", response_model=None, tags=["Channel"])
async def bulk_delete_channel(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Channel entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_channel = database.query(Channel).filter(Channel.id == item_id).first()
        if db_channel:
            database.delete(db_channel)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Channel entities"
    }

@app.put("/channel/{channel_id}/", response_model=None, tags=["Channel"])
async def update_channel(channel_id: int, channel_data: ChannelCreate, database: Session = Depends(get_db)) -> Channel:
    db_channel = database.query(Channel).filter(Channel.id == channel_id).first()
    if db_channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    setattr(db_channel, 'type', channel_data.type.value)
    setattr(db_channel, 'id', channel_data.id)
    setattr(db_channel, 'is_live', channel_data.is_live)
    setattr(db_channel, 'created_at', channel_data.created_at)
    setattr(db_channel, 'nom', channel_data.nom)
    if channel_data.match is not None:
        db_match = database.query(Match).filter(Match.id == channel_data.match).first()
        if not db_match:
            raise HTTPException(status_code=400, detail="Match not found")
        setattr(db_channel, 'match_id', channel_data.match)
    else:
        setattr(db_channel, 'match_id', None)
    if channel_data.membres is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ChannelMember).filter(ChannelMember.canal_id == db_channel.id).update(
            {ChannelMember.canal_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if channel_data.membres:
            # Validate that all IDs exist
            for channelmember_id in channel_data.membres:
                db_channelmember = database.query(ChannelMember).filter(ChannelMember.id == channelmember_id).first()
                if not db_channelmember:
                    raise HTTPException(status_code=400, detail=f"ChannelMember with id {channelmember_id} not found")

            # Update the related entities with the new foreign key
            database.query(ChannelMember).filter(ChannelMember.id.in_(channel_data.membres)).update(
                {ChannelMember.canal_id: db_channel.id}, synchronize_session=False
            )
    if channel_data.messages is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Message).filter(Message.canal_id == db_channel.id).update(
            {Message.canal_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if channel_data.messages:
            # Validate that all IDs exist
            for message_id in channel_data.messages:
                db_message = database.query(Message).filter(Message.id == message_id).first()
                if not db_message:
                    raise HTTPException(status_code=400, detail=f"Message with id {message_id} not found")

            # Update the related entities with the new foreign key
            database.query(Message).filter(Message.id.in_(channel_data.messages)).update(
                {Message.canal_id: db_channel.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_channel)

    membres_ids = database.query(ChannelMember.id).filter(ChannelMember.canal_id == db_channel.id).all()
    messages_ids = database.query(Message.id).filter(Message.canal_id == db_channel.id).all()
    response_data = {
        "channel": db_channel,
        "membres_ids": [x[0] for x in membres_ids],        "messages_ids": [x[0] for x in messages_ids]    }
    return response_data


@app.delete("/channel/{channel_id}/", response_model=None, tags=["Channel"])
async def delete_channel(channel_id: int, database: Session = Depends(get_db)):
    db_channel = database.query(Channel).filter(Channel.id == channel_id).first()
    if db_channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    database.delete(db_channel)
    database.commit()
    return db_channel


@app.get("/channel/{channel_id}/membres/", response_model=None, tags=["Channel Relationships"])
async def get_membres_of_channel(channel_id: int, database: Session = Depends(get_db)):
    """Get all ChannelMember entities related to this Channel through membres"""
    db_channel = database.query(Channel).filter(Channel.id == channel_id).first()
    if db_channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    membres_list = database.query(ChannelMember).filter(ChannelMember.canal_id == channel_id).all()

    return {
        "channel_id": channel_id,
        "membres_count": len(membres_list),
        "membres": membres_list
    }

@app.get("/channel/{channel_id}/messages/", response_model=None, tags=["Channel Relationships"])
async def get_messages_of_channel(channel_id: int, database: Session = Depends(get_db)):
    """Get all Message entities related to this Channel through messages"""
    db_channel = database.query(Channel).filter(Channel.id == channel_id).first()
    if db_channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    messages_list = database.query(Message).filter(Message.canal_id == channel_id).all()

    return {
        "channel_id": channel_id,
        "messages_count": len(messages_list),
        "messages": messages_list
    }







############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



