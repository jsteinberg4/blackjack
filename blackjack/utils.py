from blackjack.core.card import Card, CardValue

BLACKJACK = 21


def hand_value(hand: list[Card]) -> int:
    """Computes the max value of a hand.

    If the hand contains an Ace, this will return the maximum value of the hand
    which does not exceed 21.

    Ex: hand=[10 of Hearts, 9 of Diamonds, Ace of Spades]
    hand value: 30 (Aces high) or 20 (Aces low)
    Returns: 20 because Aces High would bust

    Ex: hand=[Ace of Hearts, Ace of Spades]
    Hand value: 22 (Aces high) or 12 (2nd ace low)
    Returns: 12 (because 22 would bust)
    """
    total = sum(hand)

    # Compute Aces Low if necessary
    bust = False
    aces = filter(lambda c: c.value is CardValue.ACE, hand)
    while total > BLACKJACK and not bust:
        try:
            next(aces)  # Subtract 10 if there's another Ace in the hand
            # Aces high: 11
            # Aces low: 1
            total -= 10
        except StopIteration:
            # No more aces! This is the optimal hand value
            bust = True

    return total


def blackjack_hand(hand: list[Card]) -> bool:
    """Checks for a blackjack hand.

    A blackjack hand consists of 2 cards, which are an Ace and a Face card (Jack/Queen/King).
    """
    return (
            len(hand) == 2  # Max hand length
            and any(map(Card.is_face, hand))  # One of the cards is a Face
            and any(map(lambda c: c.value is CardValue.ACE, hand))  # One card is an Ace
    )
