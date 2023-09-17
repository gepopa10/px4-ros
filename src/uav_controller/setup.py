from setuptools import setup

package_name = 'uav_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/uav_controller_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gepopa',
    maintainer_email='gpopmescu@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller_node = uav_controller.controller_node:main',
        ],
    },
)
