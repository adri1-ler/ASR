import enum
from typing import List as List_, Optional as Optional_
from sqlalchemy import (
    create_engine, Column as Column_, ForeignKey as ForeignKey_, Table as Table_, 
    Text as Text_, Boolean as Boolean_, String as String_, Date as Date_, 
    Time as Time_, DateTime as DateTime_, Float as Float_, Integer as Integer_, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped as Mapped_, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class MatchStatus(enum.Enum):
    suspendu = "suspendu"
    annule = "annule"
    en_direct = "en_direct"
    pause = "pause"
    reporte = "reporte"
    a_venir = "a_venir"
    termine = "termine"

class Surface(enum.Enum):
    gazon = "gazon"
    dur_outdoor = "dur_outdoor"
    dur_indoor = "dur_indoor"
    moquette = "moquette"
    terre_battue = "terre_battue"
    beton = "beton"

class NotificationType(enum.Enum):
    break_realise_tennis = "break_realise_tennis"
    match_commence = "match_commence"
    match_termine = "match_termine"
    but_marque_football = "but_marque_football"
    nouveau_message = "nouveau_message"
    essai_marque_rugby = "essai_marque_rugby"
    demande_ami = "demande_ami"
    set_gagne_tennis = "set_gagne_tennis"
    invitation_canal = "invitation_canal"

class SportType(enum.Enum):
    football = "football"
    tennis = "tennis"
    rugby = "rugby"

class MatchType(enum.Enum):
    simple = "simple"
    double_mixte = "double_mixte"
    equipes = "equipes"
    double = "double"

class ReactionType(enum.Enum):
    choc = "choc"
    rire = "rire"
    triste = "triste"
    coeur = "coeur"
    colere = "colere"
    feu = "feu"
    pouce_haut = "pouce_haut"

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    moderateur = "moderateur"

class LineupStatus(enum.Enum):
    provisoire = "provisoire"
    annulee = "annulee"
    officielle = "officielle"

class MatchEventType(enum.Enum):
    break_tennis = "break_tennis"
    transformation = "transformation"
    faute = "faute"
    carton_jaune = "carton_jaune"
    set_gagne = "set_gagne"
    drop = "drop"
    but = "but"
    hors_jeu = "hors_jeu"
    autre = "autre"
    jeu_gagne = "jeu_gagne"
    carton_rouge = "carton_rouge"
    mele_accordee = "mele_accordee"
    penalty = "penalty"
    tie_break = "tie_break"
    ace = "ace"
    remplacement = "remplacement"
    double_faute = "double_faute"
    essai = "essai"

class CompetitionStatus(enum.Enum):
    termine = "termine"
    en_cours = "en_cours"
    suspendue = "suspendue"
    a_venir = "a_venir"

class PositionType(enum.Enum):
    ailier = "ailier"
    milieu = "milieu"
    attaquant = "attaquant"
    demi_de_melee = "demi_de_melee"
    pilier = "pilier"
    ouvreur = "ouvreur"
    talonneur = "talonneur"
    autre = "autre"
    centre = "centre"
    deuxieme_ligne = "deuxieme_ligne"
    defenseur = "defenseur"
    arriere = "arriere"
    troisieme_ligne = "troisieme_ligne"
    gardien = "gardien"

class FriendshipStatus(enum.Enum):
    accepte = "accepte"
    en_attente = "en_attente"
    refuse = "refuse"
    bloque = "bloque"

class ChannelType(enum.Enum):
    match = "match"
    groupe_amis = "groupe_amis"
    competition = "competition"

class CompetitionFormat(enum.Enum):
    championnat = "championnat"
    coupe = "coupe"
    tournoi = "tournoi"
    phase_groupes_puis_tournoi = "phase_groupes_puis_tournoi"


# Tables definition for many-to-many relationships
competition_team = Table_(
    "competition_team",
    Base.metadata,
    Column_("equipes", ForeignKey_("team.id"), primary_key=True),
    Column_("competitions", ForeignKey_("competition.id"), primary_key=True),
)

# Tables definition
class TennisSet(Base):
    __tablename__ = "tennisset"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    numero_set: Mapped_[int] = mapped_column(Integer_)
    jeux_j1: Mapped_[int] = mapped_column(Integer_)
    jeux_j2: Mapped_[int] = mapped_column(Integer_)
    tb_points_j1: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    tb_points_j2: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    gagnant_id: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    est_termine: Mapped_[bool] = mapped_column(Boolean_)
    match_id: Mapped_[int] = mapped_column(ForeignKey_("match.id"))

class MatchPreview(Base):
    __tablename__ = "matchpreview"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    forme_domicile: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    forme_exterieur: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    h2h_victoires_dom: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    h2h_nuls: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    h2h_victoires_ext: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    absents_domicile: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    absents_exterieur: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    enjeu: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    publie_le: Mapped_[dt_datetime] = mapped_column(DateTime_)
    match_id: Mapped_[int] = mapped_column(ForeignKey_("match.id"), unique=True)

class Team(Base):
    __tablename__ = "team"
    abreviation: Mapped_[str] = mapped_column(String_(100))
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    logo_url: Mapped_[str] = mapped_column(String_(100))
    nom: Mapped_[str] = mapped_column(String_(100))
    pays: Mapped_[str] = mapped_column(String_(100))
    stade: Mapped_[str] = mapped_column(String_(100))
    ville: Mapped_[str] = mapped_column(String_(100))
    stade_domicile_id: Mapped_[int] = mapped_column(ForeignKey_("stadium.id"), nullable=True)

class Standing(Base):
    __tablename__ = "standing"
    points_concedes: Mapped_[int] = mapped_column(Integer_)
    points_marques: Mapped_[int] = mapped_column(Integer_)
    classement: Mapped_[int] = mapped_column(Integer_)
    defaites: Mapped_[int] = mapped_column(Integer_)
    difference_points: Mapped_[int] = mapped_column(Integer_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    matchs_joues: Mapped_[int] = mapped_column(Integer_)
    nuls: Mapped_[int] = mapped_column(Integer_)
    points: Mapped_[int] = mapped_column(Integer_)
    victoires: Mapped_[int] = mapped_column(Integer_)
    equipe_id: Mapped_[int] = mapped_column(ForeignKey_("team.id"))
    competition_id: Mapped_[int] = mapped_column(ForeignKey_("competition.id"))

class PreMatchOdds(Base):
    __tablename__ = "prematchodds"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    pct_victoire_dom: Mapped_[float] = mapped_column(Float_)
    pct_match_nul: Mapped_[Optional_[float]] = mapped_column(Float_, nullable=True)
    pct_victoire_ext: Mapped_[float] = mapped_column(Float_)
    source: Mapped_[str] = mapped_column(String_(100))
    updated_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    match_id: Mapped_[int] = mapped_column(ForeignKey_("match.id"), unique=True)

class Sport(Base):
    __tablename__ = "sport"
    description: Mapped_[str] = mapped_column(String_(100))
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    logo_url: Mapped_[str] = mapped_column(String_(100))
    nom: Mapped_[str] = mapped_column(String_(100))
    type: Mapped_[SportType] = mapped_column(Enum(SportType))

class LineupPlayer(Base):
    __tablename__ = "lineupplayer"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    position_match: Mapped_[str] = mapped_column(String_(100))
    numero_maillot: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    est_titulaire: Mapped_[bool] = mapped_column(Boolean_)
    est_capitaine: Mapped_[bool] = mapped_column(Boolean_)
    ordre_entree: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    lineup_id: Mapped_[int] = mapped_column(ForeignKey_("lineup.id"))
    joueur_id: Mapped_[int] = mapped_column(ForeignKey_("player.id"))

class Reaction(Base):
    __tablename__ = "reaction"
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    type: Mapped_[ReactionType] = mapped_column(Enum(ReactionType))
    message_id: Mapped_[int] = mapped_column(ForeignKey_("message.id"))
    user_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))

class Lineup(Base):
    __tablename__ = "lineup"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    formation: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    statut: Mapped_[LineupStatus] = mapped_column(Enum(LineupStatus))
    publiee_le: Mapped_[Optional_[dt_datetime]] = mapped_column(DateTime_, nullable=True)
    est_domicile: Mapped_[bool] = mapped_column(Boolean_)
    role_double: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    match_id: Mapped_[int] = mapped_column(ForeignKey_("match.id"))
    equipe_id: Mapped_[int] = mapped_column(ForeignKey_("team.id"))

class Player(Base):
    __tablename__ = "player"
    date_naissance: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    nationalite: Mapped_[str] = mapped_column(String_(100))
    nom: Mapped_[str] = mapped_column(String_(100))
    numero: Mapped_[int] = mapped_column(Integer_)
    photo_url: Mapped_[str] = mapped_column(String_(100))
    position: Mapped_[PositionType] = mapped_column(Enum(PositionType))
    prenom: Mapped_[str] = mapped_column(String_(100))
    equipe_id: Mapped_[int] = mapped_column(ForeignKey_("team.id"))
    joueur_id: Mapped_[int] = mapped_column(ForeignKey_("favoriteplayer.id"))

class Stadium(Base):
    __tablename__ = "stadium"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    nom: Mapped_[str] = mapped_column(String_(100))
    ville: Mapped_[str] = mapped_column(String_(100))
    pays: Mapped_[str] = mapped_column(String_(100))
    capacite: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    pelouse: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    photo_url: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    latitude: Mapped_[Optional_[float]] = mapped_column(Float_, nullable=True)
    longitude: Mapped_[Optional_[float]] = mapped_column(Float_, nullable=True)

class Notification(Base):
    __tablename__ = "notification"
    contenu: Mapped_[str] = mapped_column(String_(100))
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    is_read: Mapped_[bool] = mapped_column(Boolean_)
    titre: Mapped_[str] = mapped_column(String_(100))
    type: Mapped_[NotificationType] = mapped_column(Enum(NotificationType))
    user_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))

class MediaFile(Base):
    __tablename__ = "mediafile"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    url: Mapped_[str] = mapped_column(String_(100))
    filename: Mapped_[str] = mapped_column(String_(100))
    mimetype: Mapped_[str] = mapped_column(String_(100))
    taille_ko: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    alt_text: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    cible_type: Mapped_[str] = mapped_column(String_(100))
    cible_id: Mapped_[str] = mapped_column(String_(100))
    uploaded_by: Mapped_[str] = mapped_column(String_(100))
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    uploader_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"), nullable=True)

class Message(Base):
    __tablename__ = "message"
    content: Mapped_[str] = mapped_column(String_(100))
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    edited_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    is_deleted: Mapped_[bool] = mapped_column(Boolean_)
    minute_match: Mapped_[int] = mapped_column(Integer_)
    canal_id: Mapped_[int] = mapped_column(ForeignKey_("channel.id"))
    parent_id: Mapped_[int] = mapped_column(ForeignKey_("message.id"), nullable=True)
    auteur_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))

class BracketSlot(Base):
    __tablename__ = "bracketslot"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    position: Mapped_[int] = mapped_column(Integer_)
    equipe_domicile_id: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    equipe_exterieur_id: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    vainqueur_id: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    est_qualifie: Mapped_[Optional_[bool]] = mapped_column(Boolean_, nullable=True)
    tour_id: Mapped_[int] = mapped_column(ForeignKey_("tournamentround.id"))
    match_id: Mapped_[int] = mapped_column(ForeignKey_("match.id"), unique=True)

class MatchEvent(Base):
    __tablename__ = "matchevent"
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    description: Mapped_[str] = mapped_column(String_(100))
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    minute: Mapped_[int] = mapped_column(Integer_)
    type: Mapped_[MatchEventType] = mapped_column(Enum(MatchEventType))
    joueur_id: Mapped_[int] = mapped_column(ForeignKey_("player.id"), nullable=True)
    match_id: Mapped_[int] = mapped_column(ForeignKey_("match.id"))
    equipe_id: Mapped_[int] = mapped_column(ForeignKey_("team.id"), nullable=True)

class TournamentRound(Base):
    __tablename__ = "tournamentround"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    nom: Mapped_[str] = mapped_column(String_(100))
    numero: Mapped_[int] = mapped_column(Integer_)
    date_debut: Mapped_[dt_datetime] = mapped_column(DateTime_)
    date_fin: Mapped_[Optional_[dt_datetime]] = mapped_column(DateTime_, nullable=True)
    statut: Mapped_[Optional_[CompetitionStatus]] = mapped_column(Enum(CompetitionStatus), nullable=True)
    competition_id: Mapped_[int] = mapped_column(ForeignKey_("competition.id"))

class Match(Base):
    __tablename__ = "match"
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    date_heure: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    journee: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    lieu: Mapped_[str] = mapped_column(String_(100))
    progression: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    score_domicile: Mapped_[int] = mapped_column(Integer_)
    score_exterieur: Mapped_[int] = mapped_column(Integer_)
    status: Mapped_[MatchStatus] = mapped_column(Enum(MatchStatus))
    updated_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    tour_tournoi: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    type_match: Mapped_[MatchType] = mapped_column(Enum(MatchType))
    surface: Mapped_[Optional_[Surface]] = mapped_column(Enum(Surface), nullable=True)
    set_actuel: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    score_jeu_actuel: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    serveur_id: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    competition_id: Mapped_[int] = mapped_column(ForeignKey_("competition.id"))
    equipe_domicile_id: Mapped_[int] = mapped_column(ForeignKey_("team.id"))
    stade_id: Mapped_[int] = mapped_column(ForeignKey_("stadium.id"), nullable=True)
    equipe_exterieure_id: Mapped_[int] = mapped_column(ForeignKey_("team.id"))

class Friendship(Base):
    __tablename__ = "friendship"
    status: Mapped_[FriendshipStatus] = mapped_column(Enum(FriendshipStatus))
    updated_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    demandeur_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))
    receveur_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))

class FavoritePlayer(Base):
    __tablename__ = "favoriteplayer"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    added_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    notify_match: Mapped_[bool] = mapped_column(Boolean_)
    user_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))

class FavoriteTeam(Base):
    __tablename__ = "favoriteteam"
    added_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    notify_but: Mapped_[bool] = mapped_column(Boolean_)
    notify_match: Mapped_[bool] = mapped_column(Boolean_)
    user_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))
    equipe_id: Mapped_[int] = mapped_column(ForeignKey_("team.id"))

class MatchStatistics(Base):
    __tablename__ = "matchstatistics"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    sport_type: Mapped_[Optional_[SportType]] = mapped_column(Enum(SportType), nullable=True)
    possession_domicile: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    possession_exterieur: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    tirs_domicile: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    tirs_exterieur: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    tirs_cadres_domicile: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    tirs_cadres_exterieur: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    corners_domicile: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    corners_exterieur: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    fautes_domicile: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    fautes_exterieur: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    essais_domicile: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    essais_exterieur: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    transformations_domicile: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    transformations_exterieur: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    penalties_dom: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    penalties_ext: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    meles_gagnees_dom: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    meles_gagnees_ext: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    aces_j1: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    aces_j2: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    doubles_fautes_j1: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    doubles_fautes_j2: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    pct_premier_service_j1: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    pct_premier_service_j2: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    breaks_j1: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    breaks_j2: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    sets_j1: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    sets_j2: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True)
    match_id: Mapped_[int] = mapped_column(ForeignKey_("match.id"), unique=True)

class FavoriteCompetition(Base):
    __tablename__ = "favoritecompetition"
    added_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    notif_active: Mapped_[bool] = mapped_column(Boolean_)
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    competition_id: Mapped_[int] = mapped_column(ForeignKey_("competition.id"))
    user_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))

class User(Base):
    __tablename__ = "user"
    username: Mapped_[str] = mapped_column(String_(100))
    role: Mapped_[UserRole] = mapped_column(Enum(UserRole))
    avatar_url: Mapped_[str] = mapped_column(String_(100))
    bio: Mapped_[str] = mapped_column(String_(100))
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    email: Mapped_[str] = mapped_column(String_(100))
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    mot_de_passe_hash: Mapped_[str] = mapped_column(String_(100))

class Competition(Base):
    __tablename__ = "competition"
    date_debut: Mapped_[dt_datetime] = mapped_column(DateTime_)
    date_fin: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    logo_url: Mapped_[str] = mapped_column(String_(100))
    nom: Mapped_[str] = mapped_column(String_(100))
    pays: Mapped_[str] = mapped_column(String_(100))
    saison: Mapped_[str] = mapped_column(String_(100))
    format: Mapped_[CompetitionFormat] = mapped_column(Enum(CompetitionFormat))
    statut: Mapped_[CompetitionStatus] = mapped_column(Enum(CompetitionStatus))
    sport_id: Mapped_[int] = mapped_column(ForeignKey_("sport.id"))

class ChannelMember(Base):
    __tablename__ = "channelmember"
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    is_admin: Mapped_[bool] = mapped_column(Boolean_)
    joined_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    last_read_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    user_id: Mapped_[int] = mapped_column(ForeignKey_("user.id"))
    canal_id: Mapped_[int] = mapped_column(ForeignKey_("channel.id"))

class Channel(Base):
    __tablename__ = "channel"
    created_at: Mapped_[dt_datetime] = mapped_column(DateTime_)
    id: Mapped_[str] = mapped_column(String_(100), primary_key=True)
    is_live: Mapped_[bool] = mapped_column(Boolean_)
    nom: Mapped_[str] = mapped_column(String_(100))
    type: Mapped_[ChannelType] = mapped_column(Enum(ChannelType))
    match_id: Mapped_[int] = mapped_column(ForeignKey_("match.id"), nullable=True)


#--- Relationships of the tennisset table
TennisSet.match: Mapped_["Match"] = relationship("Match", back_populates="sets", foreign_keys=[TennisSet.match_id])

#--- Relationships of the matchpreview table
MatchPreview.match: Mapped_["Match"] = relationship("Match", back_populates="preview", foreign_keys=[MatchPreview.match_id])

#--- Relationships of the team table
Team.classements: Mapped_[List_["Standing"]] = relationship("Standing", back_populates="equipe", foreign_keys=[Standing.equipe_id])
Team.fans: Mapped_[List_["FavoriteTeam"]] = relationship("FavoriteTeam", back_populates="equipe", foreign_keys=[FavoriteTeam.equipe_id])
Team.evenements_equipe: Mapped_[List_["MatchEvent"]] = relationship("MatchEvent", back_populates="equipe", foreign_keys=[MatchEvent.equipe_id])
Team.joueurs: Mapped_[List_["Player"]] = relationship("Player", back_populates="equipe", foreign_keys=[Player.equipe_id])
Team.stade_domicile: Mapped_["Stadium"] = relationship("Stadium", back_populates="equipes_domicile", foreign_keys=[Team.stade_domicile_id])
Team.lineups: Mapped_[List_["Lineup"]] = relationship("Lineup", back_populates="equipe", foreign_keys=[Lineup.equipe_id])
Team.matchs_a_domicile: Mapped_[List_["Match"]] = relationship("Match", back_populates="equipe_domicile", foreign_keys=[Match.equipe_domicile_id])
Team.matchs_a_exterieur: Mapped_[List_["Match"]] = relationship("Match", back_populates="equipe_exterieure", foreign_keys=[Match.equipe_exterieure_id])
Team.competitions: Mapped_[List_["Competition"]] = relationship("Competition", secondary=competition_team, back_populates="equipes")

#--- Relationships of the standing table
Standing.equipe: Mapped_["Team"] = relationship("Team", back_populates="classements", foreign_keys=[Standing.equipe_id])
Standing.competition: Mapped_["Competition"] = relationship("Competition", back_populates="classement", foreign_keys=[Standing.competition_id])

#--- Relationships of the prematchodds table
PreMatchOdds.match: Mapped_["Match"] = relationship("Match", back_populates="cotes", foreign_keys=[PreMatchOdds.match_id])

#--- Relationships of the sport table
Sport.competitions: Mapped_[List_["Competition"]] = relationship("Competition", back_populates="sport", foreign_keys=[Competition.sport_id])

#--- Relationships of the lineupplayer table
LineupPlayer.lineup: Mapped_["Lineup"] = relationship("Lineup", back_populates="joueurs", foreign_keys=[LineupPlayer.lineup_id])
LineupPlayer.joueur: Mapped_["Player"] = relationship("Player", back_populates="apparitions", foreign_keys=[LineupPlayer.joueur_id])

#--- Relationships of the reaction table
Reaction.message: Mapped_["Message"] = relationship("Message", back_populates="reactions", foreign_keys=[Reaction.message_id])
Reaction.user: Mapped_["User"] = relationship("User", back_populates="reactions", foreign_keys=[Reaction.user_id])

#--- Relationships of the lineup table
Lineup.match: Mapped_["Match"] = relationship("Match", back_populates="compositions", foreign_keys=[Lineup.match_id])
Lineup.joueurs: Mapped_[List_["LineupPlayer"]] = relationship("LineupPlayer", back_populates="lineup", foreign_keys=[LineupPlayer.lineup_id])
Lineup.equipe: Mapped_["Team"] = relationship("Team", back_populates="lineups", foreign_keys=[Lineup.equipe_id])

#--- Relationships of the player table
Player.apparitions: Mapped_[List_["LineupPlayer"]] = relationship("LineupPlayer", back_populates="joueur", foreign_keys=[LineupPlayer.joueur_id])
Player.equipe: Mapped_["Team"] = relationship("Team", back_populates="joueurs", foreign_keys=[Player.equipe_id])
Player.evenements_joues: Mapped_[List_["MatchEvent"]] = relationship("MatchEvent", back_populates="joueur", foreign_keys=[MatchEvent.joueur_id])
Player.joueur: Mapped_["FavoritePlayer"] = relationship("FavoritePlayer", back_populates="fans", foreign_keys=[Player.joueur_id])

#--- Relationships of the stadium table
Stadium.equipes_domicile: Mapped_[List_["Team"]] = relationship("Team", back_populates="stade_domicile", foreign_keys=[Team.stade_domicile_id])
Stadium.matchs: Mapped_[List_["Match"]] = relationship("Match", back_populates="stade", foreign_keys=[Match.stade_id])

#--- Relationships of the notification table
Notification.user: Mapped_["User"] = relationship("User", back_populates="notifications", foreign_keys=[Notification.user_id])

#--- Relationships of the mediafile table
MediaFile.uploader: Mapped_["User"] = relationship("User", back_populates="medias", foreign_keys=[MediaFile.uploader_id])

#--- Relationships of the message table
Message.canal: Mapped_["Channel"] = relationship("Channel", back_populates="messages", foreign_keys=[Message.canal_id])
Message.reponses: Mapped_[List_["Message"]] = relationship("Message", back_populates="parent", foreign_keys=[Message.parent_id])
Message.reactions: Mapped_[List_["Reaction"]] = relationship("Reaction", back_populates="message", foreign_keys=[Reaction.message_id])
Message.parent: Mapped_["Message"] = relationship("Message", back_populates="reponses", foreign_keys=[Message.parent_id], remote_side=[Message.id])
Message.auteur: Mapped_["User"] = relationship("User", back_populates="messages", foreign_keys=[Message.auteur_id])

#--- Relationships of the bracketslot table
BracketSlot.tour: Mapped_["TournamentRound"] = relationship("TournamentRound", back_populates="slots", foreign_keys=[BracketSlot.tour_id])
BracketSlot.match: Mapped_["Match"] = relationship("Match", back_populates="slot", foreign_keys=[BracketSlot.match_id])

#--- Relationships of the matchevent table
MatchEvent.joueur: Mapped_["Player"] = relationship("Player", back_populates="evenements_joues", foreign_keys=[MatchEvent.joueur_id])
MatchEvent.match: Mapped_["Match"] = relationship("Match", back_populates="evenements", foreign_keys=[MatchEvent.match_id])
MatchEvent.equipe: Mapped_["Team"] = relationship("Team", back_populates="evenements_equipe", foreign_keys=[MatchEvent.equipe_id])

#--- Relationships of the tournamentround table
TournamentRound.competition: Mapped_["Competition"] = relationship("Competition", back_populates="tours", foreign_keys=[TournamentRound.competition_id])
TournamentRound.slots: Mapped_[List_["BracketSlot"]] = relationship("BracketSlot", back_populates="tour", foreign_keys=[BracketSlot.tour_id])

#--- Relationships of the match table
Match.preview: Mapped_["MatchPreview"] = relationship("MatchPreview", back_populates="match", foreign_keys=[MatchPreview.match_id])
Match.cotes: Mapped_["PreMatchOdds"] = relationship("PreMatchOdds", back_populates="match", foreign_keys=[PreMatchOdds.match_id])
Match.slot: Mapped_["BracketSlot"] = relationship("BracketSlot", back_populates="match", foreign_keys=[BracketSlot.match_id])
Match.compositions: Mapped_[List_["Lineup"]] = relationship("Lineup", back_populates="match", foreign_keys=[Lineup.match_id])
Match.competition: Mapped_["Competition"] = relationship("Competition", back_populates="matchs", foreign_keys=[Match.competition_id])
Match.equipe_domicile: Mapped_["Team"] = relationship("Team", back_populates="matchs_a_domicile", foreign_keys=[Match.equipe_domicile_id])
Match.canaux: Mapped_[List_["Channel"]] = relationship("Channel", back_populates="match", foreign_keys=[Channel.match_id])
Match.stade: Mapped_["Stadium"] = relationship("Stadium", back_populates="matchs", foreign_keys=[Match.stade_id])
Match.evenements: Mapped_[List_["MatchEvent"]] = relationship("MatchEvent", back_populates="match", foreign_keys=[MatchEvent.match_id])
Match.equipe_exterieure: Mapped_["Team"] = relationship("Team", back_populates="matchs_a_exterieur", foreign_keys=[Match.equipe_exterieure_id])
Match.statistiques: Mapped_["MatchStatistics"] = relationship("MatchStatistics", back_populates="match", foreign_keys=[MatchStatistics.match_id])
Match.sets: Mapped_[List_["TennisSet"]] = relationship("TennisSet", back_populates="match", foreign_keys=[TennisSet.match_id])

#--- Relationships of the friendship table
Friendship.demandeur: Mapped_["User"] = relationship("User", back_populates="demandes_envoyees", foreign_keys=[Friendship.demandeur_id])
Friendship.receveur: Mapped_["User"] = relationship("User", back_populates="demandes_recues", foreign_keys=[Friendship.receveur_id])

#--- Relationships of the favoriteplayer table
FavoritePlayer.user: Mapped_["User"] = relationship("User", back_populates="joueurs_favoris", foreign_keys=[FavoritePlayer.user_id])
FavoritePlayer.fans: Mapped_[List_["Player"]] = relationship("Player", back_populates="joueur", foreign_keys=[Player.joueur_id])

#--- Relationships of the favoriteteam table
FavoriteTeam.user: Mapped_["User"] = relationship("User", back_populates="equipes_favorites", foreign_keys=[FavoriteTeam.user_id])
FavoriteTeam.equipe: Mapped_["Team"] = relationship("Team", back_populates="fans", foreign_keys=[FavoriteTeam.equipe_id])

#--- Relationships of the matchstatistics table
MatchStatistics.match: Mapped_["Match"] = relationship("Match", back_populates="statistiques", foreign_keys=[MatchStatistics.match_id])

#--- Relationships of the favoritecompetition table
FavoriteCompetition.competition: Mapped_["Competition"] = relationship("Competition", back_populates="abonnes", foreign_keys=[FavoriteCompetition.competition_id])
FavoriteCompetition.user: Mapped_["User"] = relationship("User", back_populates="competitions_favorites", foreign_keys=[FavoriteCompetition.user_id])

#--- Relationships of the user table
User.messages: Mapped_[List_["Message"]] = relationship("Message", back_populates="auteur", foreign_keys=[Message.auteur_id])
User.canaux_rejoints: Mapped_[List_["ChannelMember"]] = relationship("ChannelMember", back_populates="user", foreign_keys=[ChannelMember.user_id])
User.medias: Mapped_[List_["MediaFile"]] = relationship("MediaFile", back_populates="uploader", foreign_keys=[MediaFile.uploader_id])
User.demandes_envoyees: Mapped_[List_["Friendship"]] = relationship("Friendship", back_populates="demandeur", foreign_keys=[Friendship.demandeur_id])
User.reactions: Mapped_[List_["Reaction"]] = relationship("Reaction", back_populates="user", foreign_keys=[Reaction.user_id])
User.demandes_recues: Mapped_[List_["Friendship"]] = relationship("Friendship", back_populates="receveur", foreign_keys=[Friendship.receveur_id])
User.notifications: Mapped_[List_["Notification"]] = relationship("Notification", back_populates="user", foreign_keys=[Notification.user_id])
User.equipes_favorites: Mapped_[List_["FavoriteTeam"]] = relationship("FavoriteTeam", back_populates="user", foreign_keys=[FavoriteTeam.user_id])
User.joueurs_favoris: Mapped_[List_["FavoritePlayer"]] = relationship("FavoritePlayer", back_populates="user", foreign_keys=[FavoritePlayer.user_id])
User.competitions_favorites: Mapped_[List_["FavoriteCompetition"]] = relationship("FavoriteCompetition", back_populates="user", foreign_keys=[FavoriteCompetition.user_id])

#--- Relationships of the competition table
Competition.classement: Mapped_[List_["Standing"]] = relationship("Standing", back_populates="competition", foreign_keys=[Standing.competition_id])
Competition.matchs: Mapped_[List_["Match"]] = relationship("Match", back_populates="competition", foreign_keys=[Match.competition_id])
Competition.tours: Mapped_[List_["TournamentRound"]] = relationship("TournamentRound", back_populates="competition", foreign_keys=[TournamentRound.competition_id])
Competition.abonnes: Mapped_[List_["FavoriteCompetition"]] = relationship("FavoriteCompetition", back_populates="competition", foreign_keys=[FavoriteCompetition.competition_id])
Competition.equipes: Mapped_[List_["Team"]] = relationship("Team", secondary=competition_team, back_populates="competitions")
Competition.sport: Mapped_["Sport"] = relationship("Sport", back_populates="competitions", foreign_keys=[Competition.sport_id])

#--- Relationships of the channelmember table
ChannelMember.user: Mapped_["User"] = relationship("User", back_populates="canaux_rejoints", foreign_keys=[ChannelMember.user_id])
ChannelMember.canal: Mapped_["Channel"] = relationship("Channel", back_populates="membres", foreign_keys=[ChannelMember.canal_id])

#--- Relationships of the channel table
Channel.messages: Mapped_[List_["Message"]] = relationship("Message", back_populates="canal", foreign_keys=[Message.canal_id])
Channel.match: Mapped_["Match"] = relationship("Match", back_populates="canaux", foreign_keys=[Channel.match_id])
Channel.membres: Mapped_[List_["ChannelMember"]] = relationship("ChannelMember", back_populates="canal", foreign_keys=[ChannelMember.canal_id])

# Database connection
DATABASE_URL = "sqlite:///Sports_Live_—_Football_·_Tennis_·_Rugby.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)