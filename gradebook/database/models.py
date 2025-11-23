from peewee import (
    Model,
    SqliteDatabase,
    AutoField,
    CharField,
    ForeignKeyField,
    FloatField,
    TextField,
    IntegerField,
    DateField
)

# Use in-memory database for tests; replace with file path for production
# db = SqliteDatabase(':memory:')
# TODO
db = SqliteDatabase('gradebook.db')
 
class BaseModel(Model):
    """Base model class for Peewee."""

    class Meta:
        database = db


class Class(BaseModel):
    """Represents a class/course."""

    id = AutoField()
    name = CharField(unique=True)
    start_date = DateField(null=True)
    end_date = DateField(null=True)


class Student(BaseModel):
    """Represents a student."""

    id = AutoField()
    student_number = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()


class ClassRoster(BaseModel):
    """Link between a Class and a Student."""

    id = AutoField()
    class_ref = ForeignKeyField(Class, backref="roster", on_delete="CASCADE")
    student = ForeignKeyField(Student, backref="classes", on_delete="CASCADE")

    class Meta:
        indexes = ((("class_ref", "student"), True),)  # unique constraint


class Assignment(BaseModel):
    """Represents an assignment."""

    id = AutoField()
    title = CharField()
    category = CharField()  # quiz, test, homework


class AssignmentQuestion(BaseModel):
    """Represents a question for an assignment."""

    id = AutoField()
    assignment = ForeignKeyField(Assignment, backref="questions", on_delete="CASCADE")
    text = TextField()
    point_value = FloatField()


class ClassAssignment(BaseModel):
    """Assignment assigned to a specific class."""

    id = AutoField()
    class_ref = ForeignKeyField(Class, backref="assignments", on_delete="CASCADE")
    assignment = ForeignKeyField(Assignment, backref="assigned_classes", on_delete="CASCADE")
    total_points = FloatField()

    class Meta:
        indexes = ((("class_ref", "assignment"), True),)


class StudentAssignmentScore(BaseModel):
    """Tracks a student's score on a class assignment."""

    id = AutoField()
    roster_entry = ForeignKeyField(ClassRoster, backref="scores", on_delete="CASCADE")
    class_assignment = ForeignKeyField(ClassAssignment, backref="scores", on_delete="CASCADE")
    total_score = FloatField()
    total_time = IntegerField(null=True)  # in seconds, optional
    

class StudentQuestionScore(BaseModel):
    """Stores a student's score for each question."""
    id = AutoField()
    student = ForeignKeyField(Student, backref="question_scores", on_delete="CASCADE")
    assignment_question = ForeignKeyField(AssignmentQuestion, backref="student_scores", on_delete="CASCADE")
    points_scored = FloatField()

    class Meta:
        indexes = ((("student", "assignment_question"), True),)


class AssignmentCategoryWeight(BaseModel):
    """Stores weights for assignment categories for a class."""

    id = AutoField()
    class_ref = ForeignKeyField(Class, backref="category_weights", on_delete="CASCADE")
    category = CharField()  # quiz, test, homework
    weight = FloatField()

    class Meta:
        indexes = ((("class_ref", "category"), True),)


# Create tables
db.connect()
db.create_tables([
    Class,
    Student,
    ClassRoster,
    Assignment,
    AssignmentQuestion,
    ClassAssignment,
    StudentAssignmentScore,
    AssignmentCategoryWeight,
    StudentQuestionScore
])
