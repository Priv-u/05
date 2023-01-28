@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    '''Обработчик добавления новой статьи в базу данных'''
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = d_base.add_post(request.form['name'], request.form['url'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья успешно добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=d_base.get_menu(), title='Добавление статьи')