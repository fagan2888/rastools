#!/usr/bin/env python
# vim: set et sw=4 sts=4:

import sys
import logging
import rastools.main
import rastools.rasfile

class RasInfoUtility(rastools.main.Utility):
    """%prog [options] ras-file

    This utility accepts a source RAS file from QSCAN. It extracts and prints
    the information from the RAS file's header.

    The available command line options are listed below.
    """

    def __init__(self):
        super(RasInfoUtility, self).__init__()
        self.parser.set_defaults(
            program=False,
            ranges=False,
        )
        self.parser.add_option('-p', '--program', dest='program', action='store_true',
            help="""produce output suitable for programmatic use""")
        self.parser.add_option('-r', '--ranges', dest='ranges', action='store_true',
            help="""read each channel in the file and output its range of values""")

    def main(self, options, args):
        super(RasInfoUtility, self).main(options, args)
        if len(args) != 1:
            self.parser.error('you must specify a RAS file')
        if args[0] == '-':
            f = rastools.rasfile.RasFileReader(sys.stdin, verbose=options.loglevel<logging.WARNING)
        else:
            f = rastools.rasfile.RasFileReader(args[0], verbose=options.loglevel<logging.WARNING)
        if options.program:
            sys.stdout.write('filename=%s\n' % args[0])
            sys.stdout.write('original_filename=%s\n' % f.file_name)
            sys.stdout.write('original_filename_root=%s\n' % f.file_head)
            sys.stdout.write('version_name=%s\n' % f.version)
            sys.stdout.write('version_number=%d\n' % f.version_number)
            sys.stdout.write('pid=%d\n' % f.pid)
            sys.stdout.write('x_motor=%s\n' % f.x_motor)
            sys.stdout.write('y_motor=%s\n' % f.y_motor)
            sys.stdout.write('region_filename=%s\n' % f.region)
            sys.stdout.write('start_time=%s\n' % f.start_time.isoformat())
            sys.stdout.write('stop_time=%s\n' % f.stop_time.isoformat())
            sys.stdout.write('channel_count=%d\n' % f.channel_count)
            sys.stdout.write('channel_resolution=%d,%d\n' % (f.point_count, f.raster_count))
            sys.stdout.write('count_time%f\n' % f.count_time)
            sys.stdout.write('sweep_count=%d\n' % f.sweep_count)
            sys.stdout.write('ascii_output=%d\n' % f.ascii_out)
            sys.stdout.write('pixels_per_point=%d\n' % f.pixel_point)
            sys.stdout.write('scan_direction=%d\n' % f.scan_direction)
            sys.stdout.write('scan_type=%d\n' % f.scan_type)
            sys.stdout.write('current_x_direction=%d\n' % f.current_x_direction)
            sys.stdout.write('run_number=%d\n' % f.run_number)
            if options.ranges:
                for channel in range(f.channel_count):
                    sys.stdout.write('channel_%d_min=%d\n' % (channel, f.channels[channel].min()))
                    sys.stdout.write('channel_%d_max=%d\n' % (channel, f.channels[channel].max()))
                sys.stdout.write('\n')
            sys.stdout.write('comments=\n')
            sys.stdout.write(f.comments)
            sys.stdout.write('\n')
        else:
            sys.stdout.write('File name:              %s\n' % (args[0] if args[0] != '-' else '<stdin>'))
            sys.stdout.write('Original filename:      %s\n' % f.file_name)
            sys.stdout.write('Original filename root: %s\n' % f.file_head)
            sys.stdout.write('Version name:           %s\n' % f.version)
            sys.stdout.write('Version number:         %d\n' % f.version_number)
            sys.stdout.write('PID:                    %d\n' % f.pid)
            sys.stdout.write('X-Motor name:           %s\n' % f.x_motor)
            sys.stdout.write('Y-Motor name:           %s\n' % f.y_motor)
            sys.stdout.write('Region filename:        %s\n' % f.region)
            sys.stdout.write('Start time:             %s\n' % f.start_time.strftime('%A, %d %B %Y, %H:%M:%S'))
            sys.stdout.write('Stop time:              %s\n' % f.stop_time.strftime('%A, %d %B %Y, %H:%M:%S'))
            sys.stdout.write('Channel count:          %d\n' % f.channel_count)
            sys.stdout.write('Channel resolution:     %d x %d\n' % (f.point_count, f.raster_count))
            sys.stdout.write('Count time:             %f\n' % f.count_time)
            sys.stdout.write('Sweep count:            %d\n' % f.sweep_count)
            sys.stdout.write('Produce ASCII output:   %d (%s)\n' % (f.ascii_out, ('No', 'Yes')[bool(f.ascii_out)]))
            sys.stdout.write('Pixels per point:       %d\n' % f.pixel_point)
            sys.stdout.write('Scan direction:         %d (%s)\n' % (f.scan_direction, {1: '+ve only', 2: '+ve and -ve'}[f.scan_direction]))
            sys.stdout.write('Scan type:              %d (%s)\n' % (f.scan_type, {1: 'Quick scan', 2: 'Point to point'}[f.scan_type]))
            sys.stdout.write('Current X-direction:    %d\n' % f.current_x_direction)
            sys.stdout.write('Run number:             %d\n' % f.run_number)
            if options.ranges:
                for channel in range(f.channel_count):
                    sys.stdout.write('Channel %2d range:       %d-%d%s\n' % (
                        channel,
                        f.channels[channel].min(),
                        f.channels[channel].max(),
                        ('', ' (empty)')[f.channels[channel].min() == f.channels[channel].max()]
                    ))
            sys.stdout.write('\n')
            sys.stdout.write('Comments:\n')
            sys.stdout.write(f.comments)
            sys.stdout.write('\n')
            sys.stdout.write('\n')

main = RasInfoUtility()