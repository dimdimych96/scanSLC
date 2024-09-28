# app/routes.py

from flask import render_template, flash, redirect, url_for, request, jsonify
from app import db
from app.models import Event, Package
from app.forms import EventForm, CSVUploadForm
from app import create_app
import csv
import json
from datetime import datetime

app = create_app()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная')

@app.route('/events', methods=['GET', 'POST'])
def events():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(name=form.name.data, date=form.date.data)
        db.session.add(event)
        db.session.commit()
        flash('Событие создано!')
        return redirect(url_for('events'))
    events = Event.query.order_by(Event.date).all()
    return render_template('events.html', title='События', events=events, form=form)

@app.route('/events/<int:event_id>', methods=['GET', 'POST'])
def manage_event(event_id):
    event = Event.query.get_or_404(event_id)
    csv_form = CSVUploadForm()
    package_name = request.form.get('package_name')
    if csv_form.validate_on_submit():
        file = csv_form.csv_file.data
        stream = file.stream.read().decode("UTF8")
        csv_input = csv.reader(stream.splitlines(), delimiter=',')
        next(csv_input)  # Пропуск заголовков
        for row in csv_input:
            barcode, product_name, order_number = row
            # Здесь можно добавить логику сохранения в базу данных или другую обработку
            # Для примера просто выводим данные
            print(f"Barcode: {barcode}, Product: {product_name}, Order: {order_number}")
        flash('CSV загружен успешно!')
        return redirect(url_for('manage_event', event_id=event_id))
    packages = Package.query.filter_by(event_id=event_id).all()
    return render_template('manage_event.html', title='Управление событием', event=event, csv_form=csv_form, packages=packages)

@app.route('/create_package/<int:event_id>', methods=['POST'])
def create_package(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    package_name = data.get('package_name')
    items = data.get('items')
    if not package_name or not items:
        return jsonify({'success': False, 'message': 'Пожалуйста, заполните все поля.'}), 400
    package = Package(name=package_name, event=event, items=json.dumps(items))
    db.session.add(package)
    db.session.commit()
    return jsonify({'success': True}), 200
