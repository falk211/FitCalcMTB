from flask import Flask, render_template, request
import math

app = Flask(__name__)


# Function to compute unsagged values
def compute_unsagged_values(r_sag, h_sag, s_sag, theta_h, theta_s, t_f, t_r, sag):
    sag_decimal = sag / 100.0

    # Compute sagged travel
    delta_f = sag_decimal * t_f
    delta_r = sag_decimal * t_r

    # Compute vertical and horizontal shifts
    v_f = delta_f * math.cos(math.radians(theta_h))
    h_f = delta_f * math.sin(math.radians(theta_h))

    v_r = delta_r * math.cos(math.radians(theta_s))
    h_r = delta_r * math.sin(math.radians(theta_s))

    # Compute unsagged values
    r_unsag = r_sag - h_f
    h_unsag = h_sag + v_f
    s_unsag = s_sag + h_r

    return r_unsag, h_unsag, s_unsag


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        try:
            # Get input values
            r_sag = float(request.form['r_sag'])
            h_sag = float(request.form['h_sag'])
            s_sag = float(request.form['s_sag'])
            theta_h = float(request.form['theta_h'])
            theta_s = float(request.form['theta_s'])
            t_f = float(request.form['t_f'])
            t_r = float(request.form['t_r'])
            sag = float(request.form['sag'])

            # Compute unsagged values
            r_unsag, h_unsag, s_unsag = compute_unsagged_values(r_sag, h_sag, s_sag, theta_h, theta_s, t_f, t_r, sag)

            result = {
                'r_unsag': round(r_unsag, 2),
                'h_unsag': round(h_unsag, 2),
                's_unsag': round(s_unsag, 2)
            }
        except ValueError:
            result = {'error': 'Invalid input. Please enter valid numbers.'}

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)