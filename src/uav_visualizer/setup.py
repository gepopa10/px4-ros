from setuptools import setup

package_name = 'uav_visualizer'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/uav_visualizer_launch.py']),
        ('share/' + package_name + '/resource', ['resource/uav_visualizer.rviz'])
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
            'visualizer_node = uav_visualizer.visualizer_node:main',
        ],
    },
)
