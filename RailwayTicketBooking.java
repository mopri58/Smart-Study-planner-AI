import java.util.Scanner;

public class RailwayTicketBooking {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        final int CAPACITY = 10;
        String[] passengers = new String[CAPACITY];
        int booked = 0;
        int choice = 0;

        do {
            System.out.println("\n=== RAILWAY TICKET BOOKING SIMULATOR ===");
            System.out.println("1. Book ticket\n2. View bookings\n3. Cancel ticket\n4. Check seats\n5. Exit");
            System.out.print("Choose: ");

            if (!sc.hasNextInt()) {
                System.out.println("Please enter a number.");
                sc.nextLine();
                continue;
            }
            choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    if (booked == CAPACITY) {
                        System.out.println("Train is full.");
                        break;
                    }
                    System.out.print("Passenger name: ");
                    String name = sc.nextLine().trim();
                    if (name.isEmpty()) {
                        System.out.println("Name cannot be empty.");
                        break;
                    }
                    passengers[booked++] = name;
                    System.out.println("Ticket booked. Seat number: " + booked);
                    break;
                case 2:
                    if (booked == 0) {
                        System.out.println("No bookings yet.");
                    } else {
                        for (int i = 0; i < booked; i++) {
                            System.out.println("Seat " + (i + 1) + ": " + passengers[i]);
                        }
                    }
                    break;
                case 3:
                    System.out.print("Seat number to cancel: ");
                    if (!sc.hasNextInt()) {
                        System.out.println("Enter a valid seat number.");
                        sc.nextLine();
                        break;
                    }
                    int seat = sc.nextInt();
                    sc.nextLine();
                    if (seat < 1 || seat > booked) {
                        System.out.println("Invalid seat number.");
                        break;
                    }
                    System.out.println("Cancelled ticket for " + passengers[seat - 1]);
                    for (int i = seat - 1; i < booked - 1; i++) {
                        passengers[i] = passengers[i + 1];
                    }
                    passengers[--booked] = null;
                    break;
                case 4:
                    System.out.println("Available seats: " + (CAPACITY - booked));
                    break;
                case 5:
                    System.out.println("Thank you for using the simulator.");
                    break;
                default:
                    System.out.println("Choose 1 to 5.");
            }
        } while (choice != 5);

        sc.close();
    }
}
