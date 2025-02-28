import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap
import scipy.io as sio
from matplotlib import rc
from scipy.interpolate import UnivariateSpline
import datetime
import h5py

sns.set_style("whitegrid")
sns.set_style("ticks")

rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=True)

# solid_species = ['OMzt', 'OMbzt', 'FeOOHzt', 'FeSzt', 'S8zt', 'FeS2zt', 'AlOH3zt', 'Ca3PO42zt', 'PO4adsazt', 'PO4adsbzt', 'OMSzt', 'FeOH3zt']
# solute_species = ['O2zt', 'NO3zt', 'SO4zt', 'NH4zt', 'Fe2zt', 'H2Szt', 'S0zt', 'PO4zt', 'Ca2zt',
#                   'HSzt', 'Hzt', 'OHzt', 'CO2zt', 'CO3zt', 'HCO3zt', 'NH3zt', 'H2CO3zt', 'DOM1zt', 'DOM2zt']

species_formulas = {
    'O2': r'$O_2(aq)$',
    'CH4aq': r'$CH_4(aq)$',
    'CH4g': r'$CH_4(g)$',
    'Ox': r'$O_2(aq)$',
    'OM1': r'$OM1-C$',
    'POP': r'$POP-P$',
    'C': r'$Phy(I)-P$',
    'Chl': r'$Phy(I)-P$',
    'DOP': r'$DOP-P$',
    'NO3': r'$NO_3^-$',
    'FeOH3': r'$Fe(OH)_3$',
    'FeOOH': r'$FeOOH$',
    'FeS2': r'$FeS_2$',
    'FeS': r'$FeS$',
    'Fe3': r'$Fe(III)$',
    'FeCO3': r'$FeCO_3$',
    'Fe3PO42': r'$Fe_3(PO_4)_2$',
    'SO4': r'$SO_4^{2-}$',
    'NH4': r'$NH_4^+$',
    'Fe2': r'$Fe^{2+}$',
    'H2S': r'$H_2S$',
    'HS': r'$HS$',
    'P': r'$PO_4-P$',
    'H': r'$H_3O^+$',
    'H3O': r'$H_3O^+$',
    'PO4adsa': r'$P=Fe(OH)_3$',
    'PO4adsb': r'$P=FeOOH$',
    'PO4adsc': r'$P=Al(OH)_3$',
    'PO4': r'$PO_4-P$',
    'Al3': r'$Al(OH)_3$',
    'AlOH3': r'$Al(OH)_3$',
    'PP': r'$P=Fe(III)$',
    'Ca2': r'$Ca^{2+}$',
    'CaCO3': r'$CaCO_3$',
    'CO2': r'$CO_2(aq)$',
    'CO2aq': r'$CO_2(aq)$',
    'HCO3': r'$HCO_3^{-}$',
    'CO3': r'$CO_3^{2-}$',
    'POC': r'$POC-C$',
    'DOC': r'$DOC-C$',
    'DIC': r'$DIC-C$',
    'Ca3PO42': r'$Ca_3(PO_4)_2$',
    'H_sw': r'$Hsw$',
    'H_sw_2': r'$Hsw_2$',
    'T': r'T',
    'rho': r'\rho',
    'K': r'Kz',
    'pH': r'pH',
    'OMS': r'OMS'
}

molar_masses = {
    'O2': 31998.8,
    'CH4aq': 16042.5,
    'CH4g': 16042.5,
    'Ox': 31998.8,
    'OM1': 30973.762,
    'POP': 30973.762,
    'Chl': 30973.762,
    'DOP': 30973.762,
    'NO3': 62004,
    'FeOH3': 106867.0,
    'Fe3': 106867.0,
    'SO4': 96062,
    'NH4': 18038,
    'Fe2': 55845,
    'H2S': 34080.9,
    'HS': 33072.9,
    'P': 30973.762,
    'PO4adsa': 30973.762,
    'PO4adsb': 30973.762,
    'PO4adsc': 30973.762,
    'PO4': 30973.762,
    'Al3': 78003.6,
    'PP': 30973.762,
    'Ca2': 80156.0,
    'CO2': 44009.5,
    'CO2aq': 44009.5,
    'HCO3': 61016.8,
    'CO3': 60008.9,
    'POC': 12010.7,
    'DOC': 12010.7,
    'DIC': 61016.8,
    'Ca3PO42': 310176.7,
    'Fe3PO42': 357477.7,
    'FeS': 87910.0,
    'CaCO3': 100086.9,
    'AlOH3': 78003.6
}

solid = [
    'OM', 'OMb', 'FeOH3', 'FeOOH', 'PO4adsa', 'PO4adsb', 'PO4adsc', 'OMb',
    'Ca3PO42', 'POC', 'POP', 'FeS2', 'FeS', 'Fe3PO42', 'FeCO3', 'AlOH3'
]

disolved = [
    'O2',
    'DOM1',
    'DOM2',
    'NO3',
    'SO4',
    'NH4',
    'Fe2',
    'H2S',
    'HS',
    'PO4',
    'Al3',
    'Ca2',
    'CO2',
    'CH4aq',
    'CH4g',
]

solid_rates = [
    'R1a', 'R1b', 'R1f', 'R2a', 'R2b', 'R2f', 'R3a', 'R3b', 'R3f', 'R4a', 'R4b',
    'R4f', 'R5a', 'R5b', 'R5f', 'R6a', 'R6b', 'R6f', 'Ra', 'Rb', 'Rf'
]

aqueous_rates = [
    'R1c', 'R2c', 'R3c', 'R4c', 'R5c', 'R6c', 'Rc', 'R1d', 'R2d', 'R3d', 'R4d',
    'R5d', 'R6d', 'Rd'
]


def find_element_name(element):
    return species_formulas[element]


def load_data(f):
    try:
        mat_contents = sio.loadmat(f)
    except NotImplementedError:
        import hdf5storage
        mat_contents = hdf5storage.loadmat(f)
    MyLake_results = mat_contents['MyLake_results']
    Sediment_results = mat_contents['Sediment_results']
    return MyLake_results, Sediment_results


class ResultsPlotter:
    """docstring for ResultsPlotter"""

    def __init__(self, years_ago=0., f='../IO/MyLakeResults.mat'):
        self.mat_contents = h5py.File(f)
        # self.my_lake_results = MyLake_results
        # self.sediment_results = Sediment_results
        years_ago = years_ago + 1

    def env_getter(self, env, basin=1):
        if env == 'sediment':
            results = self.mat_contents['Sediment_results']['basin'
                                                            + str(basin)]
        elif env == 'water':
            results = self.mat_contents['MyLake_results']['basin'
                                                          + str(basin)]
        return results

    def unit_converter(self, convert_units, env, elem):
        if convert_units:
            if env == 'sediment':
                coef = molar_masses[elem]
                units = '[$mg/m^3$]'
            elif env == 'water':
                coef = 1 / molar_masses[elem]
                units = '[$mmol/L$]'
        else:
            coef = 1
            if env == 'sediment':
                units = '[$mmol/L$]'
            elif env == 'water':
                units = '[$mg/m^3$]'
        return coef, units

    def flux(self,
             elem,
             convert_units=False,
             smoothing_factor=False,
             years_ago=0.):

        results = self.env_getter('sediment', basin=1)

        plt.figure(figsize=(6, 4), dpi=192)
        start = int(-365 * (years_ago + 1))
        end = int(-365 * years_ago - 1)
        x = results['days'][start:end] - 366
        y = results['sediment_transport_fluxes'][elem][start:end]
        total = {}
        lines = {}
        if convert_units:
            y = y / (molar_masses[elem] * 10**4 / 365 / 10**6)
            lbl = '[' + find_element_name(elem) + ']' + \
                ' flux, $[umol/cm^{2}/y]$'
            total['D'] = np.trapz(y, x / 365)
        else:
            lbl = '[' + find_element_name(elem) + ']' + ' flux, $[mg/m^{2}/d]$'
            total['D'] = np.trapz(y, x)
        if smoothing_factor:
            spl = UnivariateSpline(x, y)
            spl.set_smoothing_factor(smoothing_factor)
            lines['D'], = plt.plot(
                x, spl(x), sns.xkcd_rgb["denim blue"], lw=3, label='Transport')
        else:
            lines['D'], = plt.plot(
                x, y, sns.xkcd_rgb["denim blue"], lw=3, label='Transport')

        try:
            b = results['Bioirrigation_fx_zt'][elem][start:end]
            if convert_units:
                b = b / (molar_masses[elem] * 10**4 / 365 / 10**6)
            lines['B'], = plt.plot(
                x, b, sns.xkcd_rgb["medium green"], lw=3, label='Bioirrigation')
            if convert_units:
                x = x / 365
            total['B'] = np.trapz(b, x)
        except:
            pass

        if convert_units:
            lbl_2 = ' $[umol/cm^{2}]$'
        else:
            lbl_2 = ' $[mg/m^{2}]$'
        leg1 = plt.legend(
            [lines[e] for e in lines.keys()],
            ["{:.2f} ".format(total[e]) + lbl_2 for e in total.keys()],
            loc=4,
            frameon=1,
            title="Integrated over time")
        ax = plt.gca()
        ax.set_ylabel(lbl)
        ax.ticklabel_format(useOffset=False)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        ax.set_xlim([
            results['days'][start:end][0] - 366,
            results['days'][start:end][-1] - 366
        ])
        ax.grid(linestyle='-', linewidth=0.2)
        ax.legend(loc=1)
        plt.gca().add_artist(leg1)
        leg2 = plt.legend(frameon=1, loc=1)
        frame = leg2.get_frame()
        frame.set_facecolor('white')
        # frame.set_alpha(0.7)
        plt.tight_layout()
        plt.show()

    def profile(self,
                env,
                elem,
                convert_units=False,
                years_ago=0.,
                log_scale=False):
        results = self.env_getter(env)
        plt.figure(figsize=(6, 4), dpi=192)

        end = int(-365 * years_ago - 1)
        z = results['z'][:, -1]
        mass_per_area = {}
        lines = {}

        for e in elem:
            coef, units = self.unit_converter(convert_units, env, e)
            y = results['concentrations'][e][:, -1 + end] * coef
            if log_scale:
                y = np.log10(y)
            lines[e], = plt.plot(y, -z, lw=3, label=find_element_name(e))
            if convert_units and env == 'sediment':
                fi = results['params']['phi'][:, -1]
                if e in solid:
                    theta = 1 - fi
                else:
                    theta = fi
                mass_per_area[e] = np.trapz(y * theta, z / 100)
                lbl = r'$mg / m^2$'
            elif convert_units and env == 'water':
                mass_per_area[e] = np.trapz(y, z * 100)
                lbl = r'$umol/cm^{2}$'
            elif not convert_units and env == 'water':
                mass_per_area[e] = np.trapz(y, z)
                lbl = r'$mg / m^2$'
            elif not convert_units and env == 'sediment':
                fi = results['params']['phi'][:, -1]
                if e in solid:
                    theta = 1 - fi
                else:
                    theta = fi
                mass_per_area[e] = np.trapz(y * theta, z)
                lbl = r'$umol/cm^{2}$'
            if e is 'pH':
                units = r'pH'
            if e is 'Temperature':
                units = r'Temperature, C'
        if not log_scale:
            leg1 = plt.legend(
                [lines[e] for e in elem],
                ["{:.2f} ".format(mass_per_area[e]) + lbl for e in elem],
                loc=4,
                frameon=1,
                title="Integrated over depth")
        plt.xlabel(units)
        if env == 'water':
            plt.ylabel('Depth, [m]')
        else:
            plt.ylabel('Depth, [cm]')
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.grid(linestyle='-', linewidth=0.2)
        plt.legend(loc=1, frameon=1)
        if not log_scale:
            plt.gca().add_artist(leg1)
        plt.ylim([-results['z'][-1], -results['z'][0]])
        plt.tight_layout()
        date = results['days'][-1 + end]
        date = datetime.datetime.fromordinal(date - 365)
        plt.title('Profiles on ' + date.strftime('%B %d, %Y'))
        return ax

    def rate_profile(self, env, rates, years_ago=0.):
        results = self.env_getter(env)
        plt.figure(figsize=(6, 4), dpi=192)
        end = int(-365 * years_ago - 1)
        z = results['z'][:, -1]
        rate_per_area = {}
        lines = {}
        for rate in rates:
            y = results['rates'][rate][:, -1 + end]
            lines[rate], = plt.plot(y, -z, lw=3, label=rate)
            if env == 'water':
                rate_per_area[rate] = np.trapz(y, z * 100)
            elif env == 'sediment':
                fi = results['params']['phi'][:, -1]
                if rate in solid_rates:
                    theta = 1 - fi
                elif rate in aqueous_rates:
                    theta = fi
                else:
                    print('Add rate in the solid or aqueous dictionary')
                    sys.exit()
                rate_per_area[rate] = np.trapz(y * theta, z)
        lbl = r'$umol/cm^{2} / y$'
        leg1 = plt.legend(
            [lines[rate] for rate in rates],
            ["{:.2f} ".format(rate_per_area[rate]) + lbl for rate in rates],
            loc=4,
            frameon=1,
            title="Integrated over depth")
        plt.xlabel('$umol/cm^{3}/y$')
        if env == 'water':
            plt.ylabel('Depth, [m]')
        else:
            plt.ylabel('Depth, [cm]')
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.grid(linestyle='-', linewidth=0.2)
        plt.legend(loc=1, frameon=1)
        plt.gca().add_artist(leg1)
        plt.ylim([-results['z'][-1], -results['z'][0]])
        plt.tight_layout()
        plt.show()

    def contour_plot(self,
                     env,
                     elem,
                     convert_units=False,
                     years_ago=0.,
                     cmap=ListedColormap(sns.color_palette("Blues", 51))):

        results = self.env_getter(env)
        plt.figure(figsize=(6, 4), dpi=192)
        start = int(-365 * (years_ago + 1))
        end = int(-365 * years_ago - 1)
        X, Y = np.meshgrid(results['days'][start:end] - 365,
                           -results['z'][0:-1])
        z = 0
        for e in elem:
            coef, units = self.unit_converter(convert_units, env, e)
            try:
                z += results['concentrations'][e][0:-1, start:
                                                              end] * coef
            except:
                z += results[e][0:-1, start:end] * coef

        v = np.linspace(0, z.max(), 51, endpoint=True)
        CS = plt.contourf(
            X, Y, z, v, cmap=cmap, origin='lower', vmin=0,
            vmax=z.max()) # v, vmin=0, vmax=z.max()
        cbar = plt.colorbar(CS)

        plt.ylabel('Depth, [cm]')
        plt.ylim(Y.min(), 0)
        if env == 'water':
            ice_thickness = results['His'][0, start:end]
            plt.fill_between(
                results['days'][start:end] - 366,
                0,
                -ice_thickness,
                where=-ice_thickness <= 0,
                facecolor='red',
                interpolate=True)
            TCz = results['MixStat'][11, start:end]
            plt.plot(
                results['days'][start:end] - 366,
                -TCz * (TCz > 1),
                lw=0.2,
                c='k')
            plt.ylabel('Depth, [m]')

        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        lbl = ''
        for e in elem:
            lbl += find_element_name(e) + ', '
        cbar.ax.set_ylabel(lbl + units)
        if elem[0] == 'T':
            cbar.ax.set_ylabel('Temperature, [C]')
        if elem[0] == 'H_sw_zt':
            cbar.ax.set_ylabel('Light limiting function (group 1), [-]')
        if elem[0] == 'H_sw_zt_2':
            cbar.ax.set_ylabel('Light limiting function(group 2), [-]')
        plt.show()

    def custom_contour_plot(self,
                            z,
                            vmin=-3.7,
                            vmax=-3.7,
                            cmap=ListedColormap(sns.color_palette("Blues",
                                                                  51))):

        results = self.env_getter('water')
        plt.figure(figsize=(6, 4), dpi=192)
        start = int(-365)
        end = int(-1)
        X, Y = np.meshgrid(results['days'][start:end] - 365,
                           -results['z'][0:-1])

        # vmin = -3.7#-np.max(np.abs([z.min(), z.max()]))
        # vmax = 3.7#np.max(np.abs([z.min(), z.max()]))
        v = np.linspace(vmin, vmax, 51, endpoint=True)
        CS = plt.contourf(
            X, Y, z, v, cmap=cmap, origin='lower', vmin=vmin, vmax=vmax)
        cbar = plt.colorbar(CS)

        plt.ylabel('Depth, [cm]')
        plt.ylim(Y.min(), 0)

        plt.ylabel('Depth, [m]')

        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.show()

    def contour_plot_mean_several_years(self,
                                        env,
                                        elem,
                                        convert_units=False,
                                        years_ago=0.,
                                        years=1,
                                        cmap=ListedColormap(
                                            sns.color_palette("Blues", 51))):
        results = self.env_getter(env)
        plt.figure(figsize=(6, 4), dpi=192)
        start = int(-365 * (years_ago + 1))
        end = int(-365 * years_ago - 1)
        X, Y = np.meshgrid(results['days'][start:end] - 365,
                           -results['z'][0:-1])
        z = 0
        for e in elem:
            coef, units = self.unit_converter(convert_units, env, e)
            for y in range(0, years):
                try:
                    z += results['concentrations'][e][
                        0:-1, start - (y * 365):end - (y * 365)] * coef
                except:
                    z += results[e][0:-1, start - (y * 365):end -
                                          (y * 365)] * coef
            z /= years
        v = np.linspace(0, z.max(), 51, endpoint=True)
        CS = plt.contourf(
            X, Y, z, v, cmap=cmap, origin='lower', vmin=0,
            vmax=z.max()) # v, vmin=0, vmax=z.max()
        cbar = plt.colorbar(CS)

        plt.ylabel('Depth, [cm]')
        plt.ylim(Y.min(), 0)
        ice_thickness = 0
        TCz = 0
        if env == 'water':
            for y in range(0, years):
                ice_thickness += results['His'][0, start - (y * 365):end - (y * 365)]
                tcline = results['MixStat'][11, start - (y * 365):end -
                                                  (y * 365)]
                tcline[tcline == np.nan] = 0
                TCz += tcline
            ice_thickness /= years
            TCz /= years
            plt.fill_between(
                results['days'][start:end] - 366,
                0,
                -ice_thickness,
                where=-ice_thickness <= 0,
                facecolor='red',
                interpolate=True)
            plt.plot(
                results['days'][start:end] - 366,
                -TCz * (TCz > 1),
                lw=0.2,
                c='k')
            plt.ylabel('Depth, [m]')

        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        lbl = ''
        for e in elem:
            lbl += find_element_name(e) + ', '
        cbar.ax.set_ylabel(lbl + units)
        if elem[0] == 'T':
            cbar.ax.set_ylabel('Temperature, [C]')
        if elem[0] == 'H_sw_zt':
            cbar.ax.set_ylabel('Light limiting function (group 1), [-]')
        if elem[0] == 'H_sw_zt_2':
            cbar.ax.set_ylabel('Light limiting function(group 2), [-]')
        plt.show()
        return z



    def rate(self,
             env,
             elem,
             convert_units=False,
             years_ago=0.,
             cmap=ListedColormap(sns.color_palette("RdBu_r", 101))):
        results = self.env_getter(env)
        plt.figure(figsize=(6, 4), dpi=192)
        start = int(-365 * (years_ago + 1))
        end = int(-365 * years_ago - 1)
        X, Y = np.meshgrid(results['days'][start:end],
                           -results['z'])
        z = 0
        for e in elem:
            z += results['dcdt'][e][:, start:end]
        # CS = plt.contourf(X, Y, z, 51, cmap=cmap, origin='lower')
        lim = np.max(np.abs(z))
        lim = np.linspace(-lim - 1e-16, +lim + 1e-16, 51)
        CS = plt.contourf(
            X,
            Y,
            z,
            51,
            cmap=ListedColormap(sns.color_palette("RdBu_r", 101)),
            origin='lower',
            levels=lim,
            extend='both')
        #     plt.clabel(CS, inline=1, fontsize=10, colors='w')
        cbar = plt.colorbar(CS)

        plt.ylabel('Depth, [cm]')

        if env == 'water':
            ice_thickness = results['His'][0, 0][0, start:end]
            plt.fill_between(
                results['days'][0, 0][start:end],
                0,
                -ice_thickness,
                where=-ice_thickness <= 0,
                facecolor='red',
                interpolate=True)
            plt.ylabel('Depth, [m]')
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        lbl = ''
        for e in elem:
            lbl += e + ', '
        if elem[0] == 'T':
            cbar.ax.set_ylabel('Temperature, [C]')
        elif elem[0] == 'H_sw_zt':
            cbar.ax.set_ylabel('Light limiting function (group 1), [-]')
        elif elem[0] == 'H_sw_zt_2':
            cbar.ax.set_ylabel('Light limiting function(group 2), [-]')
        else:
            cbar.ax.set_ylabel('Rate ' + lbl + '$[mmol/L/y]$')
        plt.show()

    def bulk_sediment_profile(self,
                              elem,
                              convert_units=False,
                              years_ago=0.,
                              cmap=ListedColormap(
                                  sns.color_palette("RdBu_r", 101))):
        results = self.env_getter('sediment')
        plt.figure(figsize=(6, 4), dpi=192)
        end = int(-365 * years_ago - 1)
        z = results['z'][0, 0][:, -1]
        mass_per_area = {}
        lines = {}
        fi = results['params'][0, 0]['phi'][0, 0][:, -1]
        for e in elem:
            coef, units = self.unit_converter(convert_units, 'sediment', e)
            if e in disolved:
                y = results['concentrations'][0, 0][e][
                    0, 0][:, -1 + end] * coef * fi
            elif e in solid:
                y = results['concentrations'][0, 0][e][
                    0, 0][:, -1 + end] * coef * (1 - fi)
            else:
                print(
                    e +
                    " is not in solid or dissolved species. Check the dictionaries."
                )
                sys.exit()
            lines[e], = plt.plot(y, -z, lw=3, label=find_element_name(e))
            if convert_units:
                mass_per_area[e] = np.trapz(y, z / 100)
                lbl = r'$mg / m^2$'
            elif not convert_units:
                mass_per_area[e] = np.trapz(y, z)
                lbl = r'$umol/cm^{2}$'
        leg1 = plt.legend(
            [lines[e] for e in elem],
            ["{:.2f} ".format(mass_per_area[e]) + lbl for e in elem],
            loc=4,
            frameon=1,
            title="Integrated over depth")
        plt.xlabel(units)
        plt.ylabel('Depth, [cm]')
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.grid(linestyle='-', linewidth=0.2)
        plt.legend(loc=1, frameon=1)
        plt.gca().add_artist(leg1)
        plt.ylim([-results['z'][0, 0][-1], -results['z'][0, 0][0]])
        plt.tight_layout()
        date = results['days'][0, 0][-1 + end]
        date = datetime.datetime.fromordinal(date - 365)
        plt.title('Bulk profiles on ' + date.strftime('%B %d, %Y'))
        plt.show()

    def temperature_fit(self):
        results = self.env_getter('water', basin=2)
        T = results['T'][0, 0]
        t = results['days'][0, 0][0] - 366

        df = pd.read_csv('../obs/vanem_obs/temperature.txt', sep=',')
        df.rename(
            columns={r'Dato': 'date',
                     'TemperaturC': 'T',
                     'Depthm': 'z'},
            inplace=True)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna()
        unique_depths = df.z.unique()

        fig, axes = plt.subplots(
            len(unique_depths),
            1,
            sharex='col',
            figsize=(8, len(unique_depths) * 1.5),
            dpi=192)

        for i, d in enumerate(np.sort(df.z.unique())):
            inx = np.where(results['z'][0, 0] == d)[0][0]
            axes[i].plot(t, T[inx, :], c=sns.xkcd_rgb["denim blue"], lw=2)
            axes[i].plot(
                df[df.z == d].date,
                df[df.z == d]['T'],
                'bo',
                c=sns.xkcd_rgb["pale red"],
                markersize=4,
                label=str(d) + ' m')

        axes[3].xaxis.set_major_locator(mdates.MonthLocator(interval=12))
        axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        axes[1].set_xlim([732313 - 366, 735234 - 366])

        for ax in axes:
            ax.grid(linestyle='-', linewidth=0.2)
            # ax.set_ylim([0, 5])
            ax.set_ylabel(r'$[C]$')
            legend = ax.legend(frameon=1, loc=1)
            frame = legend.get_frame()
            frame.set_facecolor('white')

    def phosphorus_fit(self):
        fig, axes = plt.subplots(4, 1, sharex='col', figsize=(8, 5), dpi=192)

        results = self.env_getter('water', basin=1)

        inx = np.where(results['z'][0, 0] == 4)[0][0]
        TOTP = np.mean(results['concentrations'][0, 0]['P'][0, 0][0:inx, :], axis=0) + \
            np.mean(results['concentrations'][0, 0]['PP'][0, 0][0:inx, :], axis=0) + \
            np.mean(results['concentrations'][0, 0]['DOP'][0, 0][0:inx, :], axis=0) + \
            np.mean(results['concentrations'][0, 0]
                    ['POP'][0, 0][0:inx, :], axis=0)
        # np.mean(results['concentrations'][0, 0]['Chl'][0, 0][0:inx, :], axis=0) + \
        # np.mean(results['concentrations'][0, 0]['C'][0, 0][0:inx, :], axis=0)
        Chl = np.mean(
            results['concentrations'][0, 0]['C'][0, 0][0:inx, :],
            axis=0) + np.mean(
                results['concentrations'][0, 0]['Chl'][0, 0][0:inx, :], axis=0)
        PO4 = np.mean(
            results['concentrations'][0, 0]['P'][0, 0][0:inx, :], axis=0)

        Part = np.mean(
            results['concentrations'][0, 0]['POP'][0, 0][0:inx, :], axis=0)

        # + np.mean(results['concentrations'][0, 0]['POC'][0, 0][0:inx, :], axis=0)

        axes[0].plot(
            -366 + results['days'][0, 0][0],
            TOTP,
            c=sns.xkcd_rgb["denim blue"],
            lw=3,
            label='Total P')
        axes[1].plot(
            -366 + results['days'][0, 0][0],
            Chl,
            c=sns.xkcd_rgb["denim blue"],
            lw=3,
            label='Chl-a')
        axes[2].plot(
            -366 + results['days'][0, 0][0],
            PO4,
            c=sns.xkcd_rgb["denim blue"],
            lw=3,
            label='PO_4')
        axes[3].plot(
            -366 + results['days'][0, 0][0],
            Part,
            c=sns.xkcd_rgb["denim blue"],
            lw=3,
            label='POP')
        # axes[4].plot(-366 + results['days'][0, 0][0], np.mean(results['DOP'][0, 0][0:inx, :], axis=0), lw=3, label='DOP')
        # axes[4].plot(-366 + results['days'][0, 0][0], np.mean(results['P'][0, 0][0:inx, :], axis=0), lw=3, label='P')
        # axes[4].plot(-366 + results['days'][0, 0][0], np.mean(results['POC'][0, 0][0:inx, :], axis=0), lw=3, label='POC')

        TOTP = np.loadtxt('../obs/store_obs/TOTP.dat', delimiter=',')
        Chl = np.loadtxt(
            '../obs/store_obs/Cha_aquaM_march_2017.dat', delimiter=',')
        PO4 = np.loadtxt('../obs/store_obs/PO4.dat', delimiter=',')
        Part = np.loadtxt('../obs/store_obs/Part.dat', delimiter=',')
        axes[0].plot(
            -366 + TOTP[:, 0],
            TOTP[:, 1],
            'bo',
            c=sns.xkcd_rgb["pale red"],
            markersize=4)
        axes[1].plot(
            -366 + Chl[:, 0],
            Chl[:, 1],
            'bo',
            c=sns.xkcd_rgb["pale red"],
            markersize=4)
        axes[2].plot(
            -366 + PO4[:, 0],
            PO4[:, 1],
            'bo',
            c=sns.xkcd_rgb["pale red"],
            markersize=4)
        axes[3].plot(
            -366 + Part[:, 0],
            Part[:, 1],
            'bo',
            c=sns.xkcd_rgb["pale red"],
            markersize=4)

        axes[3].xaxis.set_major_locator(mdates.MonthLocator(interval=12))
        axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        axes[1].set_xlim([732313 - 366, 735234 - 366 * 1])

        for ax in axes:
            ax.grid(linestyle='-', linewidth=0.2)
            # ax.set_ylim([0, 50])
            ax.set_ylabel(r'$[mg / m^3]$')
            ax.legend(loc=1)

    def intime(self, env, elem, depth):
        results = self.env_getter(env)

        inx = sum(results['z'][0, 0] == depth)[0]

        for e in elem:
            y = results['concentrations'][0, 0]['P'][0, 0][inx, :]
            plt.scatter(
                -366 + results['days'][0, 0][0],
                y,
                lw=3,
                label=find_element_name(e))
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.grid(linestyle='-', linewidth=0.2)
        plt.legend()
        plt.tight_layout()
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        # ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        plt.show()

    def oxygen_fit_wc(self,
                      depth,
                      ax=None,
                      dstart='2005-03-07',
                      dend='2011-03-07'):
        self.plot_fit_wc(
            ['O2'], depth, ax=None, dstart=dstart, dend=dend, factor=1e-3)

    def plot_fit_wc(self,
                    elements,
                    depth,
                    ax=None,
                    dstart='2005-03-07',
                    dend='2011-03-07',
                    factor=1):
        env = 'water'
        results = self.env_getter(env)

        inx = np.where(results['z'][0, 0] == depth)[0][0]

        y = 0

        if elements == ['T']:
            y = results['T'][0, 0][inx, :]
            lbl = 'Temperature, C'
        else:
            for e in elements:
                y += results['concentrations'][0, 0][e][0, 0][inx, :] * factor
            lbl = ", ".join(elements) + ' concentration'

        if not ax:
            ax = plt.gca()

        ax.plot(-366 + results['days'][0, 0][0], y, lw=5, label='model')
        # ax.ticklabel_format(useOffset=False)
        ax.grid(linestyle='-', linewidth=0.2)
        plt.tight_layout()
        dend = datetime.datetime.strptime(dend, '%Y-%m-%d')
        dstart = datetime.datetime.strptime(dstart, '%Y-%m-%d')
        plt.xlim(dstart, dend)
        ax.set_xlabel('Date')
        ax.set_ylabel(lbl)
        legend = ax.legend(title='Depth: ' + str(depth) + 'm', frameon=1)
        plt.setp(legend.get_title(), fontsize='xx-small')
        return ax
