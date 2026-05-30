from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from web.app import app, reception, storage

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rooms')
def rooms():
    rooms_list = reception.get_all_rooms()
    return render_template('rooms.html', rooms=rooms_list)


@app.route('/bookings')
def bookings():
    active_bookings = reception.get_active_bookings()
    return render_template('bookings.html', bookings=active_bookings)


@app.route('/register_guest', methods=['GET', 'POST'])
def register_guest():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        contact = request.form.get('contact', '').strip()
        if name and contact:
            try:
                guest = reception.register_new_guest(name, contact)
                flash(f'Гость {guest.name} (ID: {guest.id}) успешно зарегистрирован!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Ошибка: {e}', 'danger')
        else:
            flash('Имя и телефон обязательны', 'danger')
    return render_template('register_guest.html')


@app.route('/book_room', methods=['GET', 'POST'])
def book_room():
    if request.method == 'POST':
        try:
            guest_id = request.form['guest_id']
            room_number = request.form['room_number']
            check_in_str = request.form['check_in']
            check_out_str = request.form['check_out']

            check_in = datetime.strptime(check_in_str, '%Y-%m-%d')
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d')

            booking = reception.book_room(guest_id, room_number, check_in, check_out)
            flash(f'Бронирование #{booking.id} успешно создано!', 'success')
            return redirect(url_for('bookings'))
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'danger')

    available_rooms = storage.find_available_rooms()
    guests = list(storage.guests.values())
    return render_template('book_room.html', rooms=available_rooms, guests=guests)


@app.route('/check_in', methods=['GET', 'POST'])
def check_in():
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        try:
            reception.check_in_guest(booking_id)
            flash(f'Гость заселен (бронь {booking_id})', 'success')
            return redirect(url_for('bookings'))
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')
    active_bookings = reception.get_active_bookings()
    return render_template('check_in.html', bookings=active_bookings)


@app.route('/order_service', methods=['GET', 'POST'])
def order_service():
    if request.method == 'POST':
        try:
            booking_id = request.form['booking_id']
            service_type = request.form['service_type']
            description = request.form['description']
            price = float(request.form['price'])

            order = reception.order_service(booking_id, service_type, description, price)
            flash(f'Услуга добавлена: {order}', 'success')
            return redirect(url_for('bookings'))
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')

    active_bookings = [b for b in reception.get_active_bookings() if b.status == "checked_in"]
    return render_template('order_service.html', bookings=active_bookings)


@app.route('/check_out', methods=['GET', 'POST'])
def check_out():
    if request.method == 'POST':
        try:
            booking_id = request.form['booking_id']
            payment = float(request.form['payment'])
            change = reception.check_out_guest(booking_id, payment)
            flash(f'Выселение завершено. Сдача: {change:.2f} BYN', 'success')
            return redirect(url_for('bookings'))
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')
    
    active_bookings = [b for b in reception.get_active_bookings() if b.status == "checked_in"]
    return render_template('check_out.html', bookings=active_bookings)
@app.route('/order_service/<booking_id>', methods=['GET', 'POST'])
def order_service_with_id(booking_id):
    """Добавление услуги с уже выбранным бронированием"""
    if request.method == 'POST':
        try:
            service_type = request.form['service_type']
            description = request.form['description']
            price = float(request.form['price'])

            order = reception.order_service(booking_id, service_type, description, price)
            flash(f'Услуга "{order.description}" добавлена!', 'success')
            return redirect(url_for('bookings'))
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')

    booking = storage.get_booking(booking_id)
    if not booking or booking.status != "checked_in":
        flash("Можно добавлять услуги только заселённым гостям", "danger")
        return redirect(url_for('bookings'))

    return render_template('order_service.html', booking=booking, preselected_booking_id=booking_id)


@app.route('/remove_service/<booking_id>/<order_id>')
def remove_service(booking_id, order_id):
    """Удаление услуги"""
    try:
        reception.remove_service(booking_id, order_id)
        flash('Услуга успешно удалена', 'success')
    except Exception as e:
        flash(f'Ошибка: {e}', 'danger')
    return redirect(url_for('bookings'))
@app.route('/check_in/<booking_id>')
def check_in_with_id(booking_id):
    """Прямое заселение по ID брони (с карточки)"""
    try:
        reception.check_in_guest(booking_id)
        flash(f'Гость успешно заселен (бронь #{booking_id})', 'success')
    except Exception as e:
        flash(f'Ошибка: {e}', 'danger')
    return redirect(url_for('bookings'))


@app.route('/check_out/<booking_id>', methods=['GET', 'POST'])
def check_out_with_id(booking_id):
    """Прямое выселение по ID брони"""
    if request.method == 'POST':
        try:
            payment = float(request.form['payment'])
            change = reception.check_out_guest(booking_id, payment)
            flash(f'Выселение успешно. Сдача: {change:.2f} BYN', 'success')
            return redirect(url_for('bookings'))
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')

    booking = storage.get_booking(booking_id)
    return render_template('check_out.html', booking=booking)