from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Book, User

engine = create_engine('sqlite:///library.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
		picture='https://pbs.twimg.com/profile_images/'
		'2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Books in Comedy
genre1 = Genre(user_id=1, name="Comedy")

session.add(genre1)
session.commit()

bookItem2 = Book(user_id=1, name="Finnegans Wake",
	description="riverrun, past Eve and Adam's, from swerve of shore to "
	"bend of bay, brings us by a commodius vicus of recirculation back"
	" to Howth Castle and Environs.",
	price="$7.50", genre=genre1)

session.add(bookItem2)
session.commit()


bookItem1 = Book(user_id=1, name="A Confederacy of Dunces",
	description="A green hunting cap squeezed the top of the fleshy "
	"balloon of a head. The green earflaps, full of large ears and uncut"
	" hair and the fine bristles that grew in the ears themselves, "
	"stuck out on...",
	price="$2.99", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = Book(user_id=1, name="Life", 
	description="PreambleTo begin with, the art of jigsaw puzzles seems"
	" of little substance....PART ONE, CHAPTER ONEYes, it could begin"
	" this way, right here, just like that, in a rather slow and "
	"ponderous way, in...",
	price="$5.50", genre=genre1)

session.add(bookItem2)
session.commit()

bookItem3 = Book(user_id=1, name="The Code of the Woosters",
	description="I reached out a hand from under the blankets, and "
	"rang the bell for Jeeves",
	price="$3.99", genre=genre1)

session.add(bookItem3)
session.commit()

bookItem4 = Book(user_id=1, name="Cold Comfort Farm",
	description="The education bestowed upon Flora Poste by her parents"
	" had been expensive, athletic and prolonged; and when they died "
	"within a few weeks of one another during the annual epidemic of "
	"influenza or...",
	price="$7.99", genre=genre1)

session.add(bookItem4)
session.commit()

bookItem5 = Book(user_id=1, name="Three Men in a Boat",
	description="There were four of us - George, and William Samuel "
	"Harris, and myself, and Montmorency.",
	price="$1.99", genre=genre1)

session.add(bookItem5)
session.commit()

bookItem6 = Book(user_id=1, name="The Diary of a Nobody",
	description="My dear wife Carrie and I have just been a week in our"
	" new house, The Laurels, Brickfield Terrace, Holloway -- a nice "
	"six-roomed residence, not counting basement, with a front "
	"breakfast-parlour.",
	price="$.99", genre=genre1)

session.add(bookItem6)
session.commit()

bookItem7 = Book(user_id=1, name="Mort",
	description="This is the bright candlelit room where the lifetimers "
	"are stored - shelf upon shelf of them, squat hourglasses, one for "
	"ever living person, pouring their fine sand from the future into"
	" the past.",
	price="$3.49", genre=genre1)

session.add(bookItem7)
session.commit()

# Books in Drama
genre1 = Genre(user_id=1, name="Drama")

session.add(genre1)
session.commit()


bookItem1 = Book(user_id=1, name="Waiting for Godot",
	description="Estragon, sitting on a low mound, is trying to take off"
	" his boot. He pulls at it with both hands, panting. He gives up, "
	"exhausted, rests, tries again. As before",
	price="$7.99", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = Book(user_id=1, name="Hunger",
	description="It was in those days when I wandered about hungry in"
	" Kristiania, that strange city which no one leaves before it has"
	" set his mark upon him...",
	price="$25", genre=genre1)

session.add(bookItem2)
session.commit()

bookItem3 = Book(user_id=1, name="Four Plays",
	description="The Bald Soprano: Anti-play Scene: A middle class"
	" English interior, with English armchairs.",
	price="$15", genre=genre1)

session.add(bookItem3)
session.commit()

bookItem4 = Book(user_id=1, name="Cider with Rosie",
	description="I was set down from the carrier's cart at the age of "
	"three; and there with a sense of bewilderment and terror my life"
	" in the village began.",
	price="$12", genre=genre1)

session.add(bookItem4)
session.commit()

bookItem5 = Book(user_id=1, name="Hamlet",
	description="Act 1, Scene 1 Enter Barnardo and Francisco, two "
	"sentinels. Barnardo Who's there?",
	price="$14", genre=genre1)

session.add(bookItem5)
session.commit()

bookItem6 = Book(user_id=1, name="The Kite Runner",
	description="I became what I am today at the age of twelve, on"
	" a frigid overcast day in the winter of 1975.",
	price="$12", genre=genre1)

session.add(bookItem6)
session.commit()


# Books in Epic
genre1 = Genre(user_id=1, name="Epic")

session.add(genre1)
session.commit()


bookItem1 = Book(user_id=1, name="The Lord of the Rings",
	description="When Mr. Bilbo Baggins of Bag End announced that he "
	"would shortly be celebrating his eleventy-first birthday with a"
	" party of special magnificence, there was much talk and excitement"
	" in Hobbiton.",
	price="$8.99", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = Book(user_id=1, name="In Search of Lost Time",
	description="For a long time, I would go to bed early.",
	price="$6.99", genre=genre1)

session.add(bookItem2)
session.commit()

bookItem3 = Book(user_id=1, name="Paradise Lost",
	description="Paradise Lost is, among other things, a poem about "
	"civil war. Satan raises 'impious war in Heav'n' by leading a "
	"third of the angels in revolt against God. The term 'impious war'"
	" implies that civil war is impious. But Milton applauded the "
	"English people for having the courage to depose and execute King"
	" Charles I. In his poem, however, he takes the side of 'Heav'n's"
	" awful Monarch'.",
	price="$9.95", genre=genre1)

session.add(bookItem3)
session.commit()

bookItem4 = Book(user_id=1, name="Hawaii",
	description="Millions upon millions of years ago, when the "
	"continents were already formed and the principal features of "
	"the earth had been decided, there existed, then as now, one "
	"aspect of the world that...",
	price="$6.99", genre=genre1)

session.add(bookItem4)
session.commit()

# Books in Science Fiction
genre1 = Genre(user_id=1, name="Science Fiction")

session.add(genre1)
session.commit()


bookItem1 = Book(user_id=1, name="Nineteen Eighty-Four",
	description="It was a bright cold day in April, and the clocks were"
	" striking thirteen.",
	price="$2.99", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = Book(user_id=1, name="Brave New World",
	description="A squat grey building of only thirty-four stories.",
	price="$5.99", genre=genre1)

session.add(bookItem2)
session.commit()

bookItem3 = Book(user_id=1, name="Slaughterhouse-Five",
	description="All this happened, more or less.",
	price="$4.50", genre=genre1)

session.add(bookItem3)
session.commit()

bookItem4 = Book(user_id=1, name="The Hitchhiker's Guide to the Galaxy",
	description="Far out in the uncharted backwaters of the unfashionable"
	" end of the Western Spiral arm of the Galaxy lies a small "
	"unregarded yellow sun. Orbiting this at a distance of roughly "
	"ninety-eight million...",
	price="$6.95", genre=genre1)

session.add(bookItem4)
session.commit()

bookItem5 = Book(user_id=1, name="The Handmaid's Tale",
	description="We slept in what had once been the gymnasium.",
	price="$7.95", genre=genre1)

session.add(bookItem5)
session.commit()

bookItem2 = Book(user_id=1, name="A Clockwork Orange",
	description="What's it going to be then, eh?",
	price="$6.80", genre=genre1)

session.add(bookItem2)
session.commit()


# Books in Mythology
genre1 = Genre(user_id=1, name="Mythology")

session.add(genre1)
session.commit()


bookItem1 = Book(user_id=1, name="The Histories",
	description="This is the showing forth of the Inquiry of Herodotus"
	" of Halicarnassos so that neither the deeds of men may be "
	"forgotten by lapse of time, nor the works great and marvellous, "
	"which have been...",
	price="$13.95", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = Book(user_id=1, name="The Odyssey",
	description="By now the other warriors, those that had escaped "
	"headlong ruin by sea or in battle, were safely home.Sing to me "
	"of the man, Muse, the man of twists and turns driven time and "
	"again off course, once...",
	price="$4.95", genre=genre1)

session.add(bookItem2)
session.commit()

# Books in Romance
genre1 = Genre(user_id=1, name="Romance")

session.add(genre1)
session.commit()


bookItem1 = Book(user_id=1, name="The Great Gatsby",
	description="In my younger and more vulnerable years my father gave"
	" me some advice that I've been turning over in my mind ever since",
	price="$9.95", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = Book(user_id=1, name="Lolita",
	description="Lolita, light of my life, fire of my loins. My sin, "
	"my soul. Lo-lee-ta: the tip of the tongue taking a trip of three"
	" steps down the palette to tap, at three, on the teeth.",
	price="$7.95", genre=genre1)

session.add(bookItem2)
session.commit()

bookItem3 = Book(user_id=1, name="Gone with the Wind",
	description="Scarlett O'Hara was not beautiful, but men seldom "
	"realized it when caught by her charm, as the Tarleton twins were",
	price="$6.50", genre=genre1)

session.add(bookItem3)
session.commit()

bookItem4 = Book(user_id=1, name="Middlemarch",
	description="Who that cares much to know the history of man, and"
	" how the mysterious mixture behaves under the varying experiments"
	" of Time, has not dwelt, at least briefly, on the life of "
	"Saint Theresa, has not..",
	price="$6.75", genre=genre1)

session.add(bookItem4)
session.commit()

bookItem2 = Book(user_id=1, name="Anna Karenina",
	description="Happy families are all alike; every unhappy family "
	"is unhappy in its own way. (C. Garnett, 1946) and "
	"(J. Carmichael, 1960)All happy families resemble one another,"
	" but each unhappy family is unhappy..",
	price="$7.00", genre=genre1)

session.add(bookItem2)
session.commit()


# Books in Magical Realism
genre1 = Genre(user_id=1, name="Magical Realism")

session.add(genre1)
session.commit()

bookItem9 = Book(user_id=1, name="Beloved",
	description="124 was spiteful. Full of baby's venom. The women "
	"in the house knew it and so did the children.",
	price="$8.99", genre=genre1)

session.add(bookItem9)
session.commit()


bookItem1 = Book(user_id=1, name="One Hundred Years of Solitude",
	description="Many years later, as he faced the firing squad, "
	"Colonel Aureliano Buendia was to remember that distant afternoon"
	" when his father took him to discover ice.",
	price="$2.99", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = Book(user_id=1, name="Midnight's Children",
	description="I was born in the city of Bombay . . . once upon a time.",
	price="$10.95", genre=genre1)

session.add(bookItem2)
session.commit()

bookItem3 = Book(user_id=1, name="Song of Solomon",
	description="The North Carolina Mutual Life Insurance agent "
	"promised to fly from Mercy to the other side of Lake Superior"
	" at three o'clock.",
	price="$7.50", genre=genre1)

session.add(bookItem3)
session.commit()

bookItem4 = Book(user_id=1, name="The Tin Drum",
	description="Granted: I'm an inmate of a mental institution; my"
	" keeper watches me, scarcely lets me out of his sight; for "
	"there's a peephole in the door, and my keeper's eye is the "
	"shade of brown that can't see...",
	price="$8.95", genre=genre1)

session.add(bookItem4)
session.commit()

bookItem2 = Book(user_id=1, name="Love in The Time of Cholera",
	description="It was inevitable: the scent of bitter almonds "
	"always reminded him of the fate of unrequited love.",
	price="$9.50", genre=genre1)

session.add(bookItem2)
session.commit()

bookItem10 = Book(user_id=1, name="Spinach Ice Cream",
	description="vanilla ice cream made with organic spinach leaves",
	price="$1.99", genre=genre1)

session.add(bookItem10)
session.commit()


# Books in Short Stories
genre1 = Genre(user_id=1, name="Short Stories")

session.add(genre1)
session.commit()


bookItem1 = Book(user_id=1, name="Dubliners",
	description="The Sisters - There was no hope for him this time:"
	" it was the third stroke.An encounter: It was Joe Dillon who "
	"introduced the Wild West to us.Araby: North Richmond Street, "
	"being blind, was a quiet...",
	price="$5.95", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = Book(user_id=1, name="Ficciones",
	description="I owe the discovery of Uqbar to the conjunction of a "
	"mirror and an encyclopedia.",
	price="$7.99", genre=genre1)

session.add(bookItem2)
session.commit()

print "added books to the library!"
